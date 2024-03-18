import math
import re
import numpy as np

from .utils.constants import STOP_WORDS


class PorterStemmer:
    def stem(self, word):
        """
        Apply the Porter Stemmer algorithm to a word and return the stemmed word.
        """
        # Step 1a
        if word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("ies"):
            word = word[:-2]
        elif word.endswith("ss"):
            pass
        elif word.endswith("s"):
            word = word[:-1]

        # Step 1b
        if word.endswith("eed"):
            if len(re.findall(r"[aeiou]", word[:-3])) > 0:
                word = word[:-1]
        elif re.search(r"([aeiou].*?)(ed|ing)$", word):
            stem = re.sub(r"([aeiou].*?)(ed|ing)$", r"\1", word)
            if re.search(r"[aeiou]", stem):
                word = stem
                if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                    word += "e"
                elif len(re.findall(r"[^aeiou]([aeiou][^aeioulsz])$", word)) == 1:
                    word = word[:-1]
                elif len(re.findall(r"([aeiou][^aeioulsz])$", word)) == 1:
                    word += "e"

        # Step 1c
        if re.search(r"([aeiou][^aeiou])y$", word):
            word = re.sub(r"([aeiou][^aeiou])y$", r"\1i", word)

        # Step 2
        if len(word) > 1:
            word = re.sub(
                r"(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti)$",
                r"\1",
                word,
            )
            if re.search(r"(alli|ousli|fulli|entli)$", word):
                word = word[:-2]
            elif re.search(
                r"(ational|tional|alize|icate|iciti|ative|ical|ness|ful)$", word
            ):
                word = word[:-4]
            elif re.search(r"(ic|ative|al|ive)$", word):
                word = word[:-3]

        # Step 3
        if len(word) > 1:
            word = re.sub(r"ness$", "", word)
            if re.search(
                r"(ational|tional|ate|iciti|ical|ance|ence|ize|ive|ous|ful)$", word
            ):
                word = word[:-4]

        # Step 4
        if len(word) > 1:
            if re.search(
                r"(ement|ment|able|ible|ance|ence|ate|iti|ion|al|er|ic|ou|ive)$", word
            ):
                word = word[:-3]
            elif re.search(r"(ant|ent|ism|ate|iti|ous|ive|ize)$", word):
                word = word[:-2]
            elif re.search(r"e$", word):
                if len(word) > 2 or len(re.findall(r"[aeiou]", word[:-1])) > 1:
                    word = word[:-1]

        # Step 5a
        if re.search(r"[aeiou].*([st])$", word):
            word = word[:-1]

        # Step 5b
        if len(re.findall(r"[aeiou].*[aeiou].*[lsz]$", word)) > 1:
            word = word[:-1]

        return word


class TextAnalyzer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.cleaned_documents = []
        self.vocabulary = []

    def clean_special_characters(self, word):
        pattern = r"[^\w\s]"
        cleaned_word = re.sub(pattern, "", word)
        return cleaned_word

    def calculate_term_frequency(self, terms_list):
        term_freq_dict = {}
        total_terms = len(terms_list)
        for term in terms_list:
            term = self.clean_special_characters(term)
            if term not in term_freq_dict:
                term_freq_dict[term] = 0
            term_freq_dict[term] += 1 / total_terms
        return term_freq_dict

    def calculate_inverse_document_frequency(self, term):
        term = self.clean_special_characters(term).strip().lower()
        num_docs_with_term = sum(
            1 for doc in self.cleaned_documents if term in doc.lower()
        )

        if num_docs_with_term > 0:
            log_result = 1 + math.log(
                len(self.cleaned_documents) / num_docs_with_term
            )  # 1 is added for smoothing
            return log_result
        else:
            return 0

    def preprocess_document(self, document):
        terms_list = re.split(r"[,\s|]+", document)
        cleaned_terms = [
            self.stemmer.stem(self.clean_special_characters(term).lower())
            for term in terms_list
            if term.lower() not in STOP_WORDS
        ]
        return cleaned_terms

    def clean_documents(self, documents_dict):
        self.cleaned_documents = [
            " ".join(self.preprocess_document(doc)) for doc in documents_dict.values()
        ]
        self.vocabulary = list(
            set([term for doc in self.cleaned_documents for term in doc.split()])
        )

    def generate_document_vector(self, document):
        terms_list = self.preprocess_document(document)
        tfidf_vector = np.zeros(len(self.vocabulary))
        term_freq = self.calculate_term_frequency(terms_list)

        for i, term in enumerate(self.vocabulary):
            term = self.clean_special_characters(term)
            if term in term_freq:
                tfidf_vector[i] = term_freq[
                    term
                ] * self.calculate_inverse_document_frequency(term)
        return tfidf_vector

    def cosine_similarity(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_vec1 = np.linalg.norm(vector1)
        norm_vec2 = np.linalg.norm(vector2)

        # Check for zero division
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        else:
            return dot_product / (norm_vec1 * norm_vec2)

    def pearson_similarity(self, vector1, vector2):
        mean_vec1 = np.mean(vector1)
        mean_vec2 = np.mean(vector2)

        # Compute Pearson correlation coefficient
        numerator = np.sum((vector1 - mean_vec1) * (vector2 - mean_vec2))
        denominator = np.sqrt(np.sum((vector1 - mean_vec1) ** 2)) * np.sqrt(
            np.sum((vector2 - mean_vec2) ** 2)
        )
        if denominator == 0:
            return 0.0
        else:
            return numerator / denominator

    def get_recommendations(self, search_history, documents, model="cosine"):
        self.clean_documents(documents)
        tfidf_matrix = []

        for key, doc in documents.items():
            tfidf_vector = self.generate_document_vector(doc)
            tfidf_matrix.append((key, tfidf_vector))

        search_tfidf = self.generate_document_vector(search_history)
        similarities = []
        for _, doc_tfidf in tfidf_matrix:
            if model == "cosine":
                similarities.append(self.cosine_similarity(search_tfidf, doc_tfidf))
            else:
                similarities.append(self.pearson_similarity(search_tfidf, doc_tfidf))

        sorted_indices = np.argsort(similarities)[::-1]

        recommendations = [
            (tfidf_matrix[i][0], similarities[i]) for i in sorted_indices
        ]
        return recommendations

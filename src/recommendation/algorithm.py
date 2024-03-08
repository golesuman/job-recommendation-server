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


class CosineSimilarity:
    def __init__(self):
        self.results = []

    def get_top_n(self, n):
        sorted_result = sorted(self.results, reverse=True)
        return sorted_result[:n]

    def dot_product(self, vector1, vector2):
        len_vector1, len_vector2 = len(vector1), len(vector2)

        if len_vector1 < len_vector2:
            vector1 = np.concatenate((vector1, np.zeros(len_vector2 - len_vector1)))
        elif len_vector2 < len_vector1:
            vector2 = np.concatenate((vector2, np.zeros(len_vector1 - len_vector2)))

        return np.dot(vector1, vector2)

    def magnitude(self, vector):
        return np.linalg.norm(vector)

    def cosine_similarity(self, doc1, doc2):
        dot_product_value = self.dot_product(doc1, doc2)
        magnitude_doc1 = self.magnitude(doc1)
        magnitude_doc2 = self.magnitude(doc2)

        if magnitude_doc1 == 0 or magnitude_doc2 == 0:
            return 0  # To handle division by zero

        return dot_product_value / (magnitude_doc1 * magnitude_doc2)


class PearsonCorrelation:
    def pearson_correlation(self, x, y):
        vector1 = np.array(x)
        vector2 = np.array(y)

        len_vector1, len_vector2 = len(vector1), len(vector2)

        if len_vector1 < len_vector2:
            vector1 = np.concatenate((vector1, np.zeros(len_vector2 - len_vector1)))
        elif len_vector2 < len_vector1:
            vector2 = np.concatenate((vector2, np.zeros(len_vector1 - len_vector2)))

        mean_x = np.mean(x)
        mean_y = np.mean(y)

        covariance = np.sum((vector1 - mean_x) * (vector2 - mean_y))
        var_x = np.sum((vector1 - mean_x) ** 2)
        var_y = np.sum((vector2 - mean_y) ** 2)
        
        if int(covariance) == 0:
            return 0

        correlation_coefficient = np.divide(
            covariance, (np.sqrt(var_x) * np.sqrt(var_y))
        )

        return correlation_coefficient


class TFIDF:
    def __init__(self, documents) -> None:
        self.documents = documents
        self.cleaned_documents = None
        self.stemmer = PorterStemmer()

    def get_tf_idf_matrix(self):
        tf_idf_matrix = self.calculate_tfidf()
        return tf_idf_matrix

    def remove_special_characters(self, word):
        pattern = r"[^\w\s]"
        cleaned_word = re.sub(pattern, "", word)
        return cleaned_word

    def calculate_tf(self, terms):
        tf_dict = {}
        total_terms = len(terms)
        for term in terms:
            term = self.remove_special_characters(term)
            if term not in tf_dict:
                tf_dict[term] = 0
            tf_dict[term] += 1 / total_terms
        return tf_dict

    def calculate_idf(self, term):
        term = self.remove_special_characters(term).strip().lower()
        self.clean_documents()
        num_documents_with_term = sum(
            1 for document in self.cleaned_documents if term in document.lower()
        )

        if num_documents_with_term > 0:
            log_result = 1 + math.log(
                len(self.documents) / num_documents_with_term
            )  # 1 is added for smoothing
            return log_result
        else:
            return 0

    def calculate_tfidf(self):
        tf_idf_matrix = []
        for key, document in self.documents.items():
            tf_idf_vector = self.fit_document(document)
            tf_idf_matrix.append((key, tf_idf_vector))
        return tf_idf_matrix

    def fit_document(self, document):
        terms = self.preprocess(document)
        # Initialize with zeros
        tf_idf_vector = np.zeros(len(terms))
        tf = self.calculate_tf(terms)

        for i, term in enumerate(terms):
            term = self.remove_special_characters(term)
            if term in tf:
                tf_idf_vector[i] = tf[term] * self.calculate_idf(term)
        return tf_idf_vector

    def preprocess(self, document):
        terms = re.split(r'[,\s]+', document)
        cleaned_terms = [
            self.stemmer.stem(self.remove_special_characters(term))
            for term in terms
            if term not in STOP_WORDS
        ]
        return cleaned_terms

    def clean_documents(self):
        if self.cleaned_documents is None:
            self.cleaned_documents = [
                self.remove_special_characters(document)
                for document in list(self.documents.values())
            ]

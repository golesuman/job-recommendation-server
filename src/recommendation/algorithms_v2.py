import math
import re
import numpy as np

from .utils.constants import STOP_WORDS


class PorterStemmer:
    def __init__(self):
        self.vowels = ["a", "e", "i", "o", "u"]
        self.step1a_suffixes = ["sses", "ies", "ss", "s"]
        self.step1b_suffixes = ["eed", "ed", "ing"]
        self.step2_suffixes = ["at", "bl", "iz"]
        self.step3_suffixes = ["ational", "ate", "tional", "tion"]
        self.step4_suffixes = ["alize", "icate", "iciti", "ical", "ful", "ness"]
        self.step5a_suffixes = [
            "al",
            "ance",
            "ence",
            "er",
            "ic",
            "able",
            "ible",
            "ant",
            "ement",
            "ment",
            "ent",
        ]
        self.step5b_suffixes = ["e", "l"]

    def stem(self, word):
        if len(word) < 3:
            return word

        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)

        return word

    def step1a(self, word):
        for suffix in self.step1a_suffixes:
            if word.endswith(suffix):
                if suffix == "sses" or suffix == "ies":
                    if len(word) > len(suffix):
                        return word[:-2]
                    else:
                        return word
                else:
                    return word[:-1]
        return word

    def step1b(self, word):
        for suffix in self.step1b_suffixes:
            if word.endswith(suffix):
                if suffix == "eed":
                    if self.count_consonant_sequences(word[:-3]) > 0:
                        return word[:-1]
                    else:
                        return word
                elif self.contains_vowel(word[: -len(suffix)]):
                    return self.stem(word[: -len(suffix)])
                else:
                    return word
        return word

    def step2(self, word):
        for suffix in self.step2_suffixes:
            if word.endswith(suffix):
                stem = word[: -len(suffix)]
                if self.count_consonant_sequences(stem) > 0:
                    return stem
                else:
                    return word
        return word

    def step3(self, word):
        for suffix in self.step3_suffixes:
            if word.endswith(suffix):
                stem = word[: -len(suffix)]
                if self.count_consonant_sequences(stem) > 0:
                    return stem
                else:
                    return word
        return word

    def step4(self, word):
        for suffix in self.step4_suffixes:
            if word.endswith(suffix):
                stem = word[: -len(suffix)]
                if self.count_consonant_sequences(stem) > 1:
                    return stem
                else:
                    return word
        return word

    def step5a(self, word):
        for suffix in self.step5a_suffixes:
            if word.endswith(suffix):
                stem = word[: -len(suffix)]
                if self.count_consonant_sequences(stem) > 1:
                    return stem
                else:
                    return word
        return word

    def step5b(self, word):
        if word.endswith("ll") and self.count_consonant_sequences(word[:-1]) > 1:
            return word[:-1]
        return word

    def count_consonant_sequences(self, word):
        count = 0
        vowels = self.vowels
        for i in range(len(word)):
            if word[i] not in vowels and (i == 0 or word[i - 1] in vowels):
                count += 1
        return count

    def contains_vowel(self, word):
        vowels = self.vowels
        for char in word:
            if char in vowels:
                return True
        return False


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
        return 1 + math.log(
            len(self.cleaned_documents) / (num_docs_with_term + 1)
        )  # 1 is added for smoothing

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

    def get_recommendations(self, data, documents, model="cosine"):
        self.clean_documents(documents)
        tfidf_matrix = []

        for key, doc in documents.items():
            tfidf_vector = self.generate_document_vector(doc)
            tfidf_matrix.append((key, tfidf_vector))

        tf_idf_vector = self.generate_document_vector(data)
        similarities = []
        for _, doc_tfidf in tfidf_matrix:
            if model == "cosine":
                similarities.append(self.cosine_similarity(tf_idf_vector, doc_tfidf))
            else:
                similarities.append(self.pearson_similarity(tf_idf_vector, doc_tfidf))

        sorted_indices = np.argsort(similarities)[::-1]

        recommendations = [
            (tfidf_matrix[i][0], similarities[i]) for i in sorted_indices
        ]
        return recommendations

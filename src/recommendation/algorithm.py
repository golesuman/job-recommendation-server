import math
import re
import numpy as np
from .utils.constants import STOP_WORDS


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

        correlation_coefficient = np.divide(
            covariance, (np.sqrt(var_x) * np.sqrt(var_y))
        )

        return correlation_coefficient


class TFIDF:
    def __init__(self, documents) -> None:
        self.documents = documents
        self.cleaned_documents = None

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
        terms = document.split(",")
        cleaned_terms = [
            self.remove_special_characters(term)
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

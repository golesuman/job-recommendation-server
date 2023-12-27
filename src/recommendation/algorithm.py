import math
import re


class CosineSimilarity:
    def __init__(self, documents) -> None:
        # pass
        self.results = []
        self.documents = documents
        # return

    def get_top_n(self, n):
        sorted_result = sorted(self.results, reverse=True)
        return sorted_result[:n]
        # pass

    def preprocess(self, document):
        # Tokenization: Split the document into words (terms)
        terms = document.lower().split()
        return terms

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
        term = self.remove_special_characters(term)
        num_documents_with_term = sum(
            1 for document in list(self.documents.values()) if term in document
        )
        if num_documents_with_term > 0:
            return math.log(len(self.documents) / num_documents_with_term)
        else:
            return 0

    def fit_document(self, document):
        terms = self.preprocess(document)
        tf = self.calculate_tf(terms)
        # print(list(self.documents.values()))
        tf_idf_vector = [
            tf[self.remove_special_characters(term)] * self.calculate_idf(term)
            for term in terms
        ]
        return tf_idf_vector

    def calculate_tfidf(self):
        tf_idf_matrix = []
        for key, document in self.documents.items():
            tf_idf_vector = self.fit_document(document)
            tf_idf_matrix.append((key, tf_idf_vector))
        return tf_idf_matrix

    def dot_product(self, vector1, vector2):
        return sum(x * y for x, y in zip(vector1, vector2))

    def magnitude(self, vector):
        return math.sqrt(sum(x**2 for x in vector))

    def cosine_similarity(self, doc1, doc2):
        dot_product_value = self.dot_product(doc1, doc2)
        magnitude_doc1 = self.magnitude(doc1)
        magnitude_doc2 = self.magnitude(doc2)

        if magnitude_doc1 == 0 or magnitude_doc2 == 0:
            return 0  # To handle division by zero

        return dot_product_value / (magnitude_doc1 * magnitude_doc2)

    def get_tf_idf_matrix(self):
        tf_idf_matrix = self.calculate_tfidf()
        return tf_idf_matrix

    def remove_special_characters(self, word):
        # Define a regular expression pattern to match special characters
        pattern = r"[^a-zA-Z0-9]"

        # Use re.sub() to replace matched special characters with an empty string
        cleaned_word = re.sub(pattern, "", word)

        return cleaned_word


class KNN:
    def __init__(self) -> None:
        pass

    def distance(self):
        pass


class TFIDF:
    def __init__(self) -> None:
        pass

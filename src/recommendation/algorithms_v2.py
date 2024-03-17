import math
import re
import numpy as np

from .algorithm import PorterStemmer
from .utils.constants import STOP_WORDS

stemmer = PorterStemmer()


def clean_special_characters(word):
    pattern = r"[^\w\s]"
    cleaned_word = re.sub(pattern, "", word)
    return cleaned_word


def calculate_term_frequency(terms_list):
    term_freq_dict = {}
    total_terms = len(terms_list)
    for term in terms_list:
        term = clean_special_characters(term)
        if term not in term_freq_dict:
            term_freq_dict[term] = 0
        term_freq_dict[term] += 1 / total_terms
    return term_freq_dict


def calculate_inverse_document_frequency(term, cleaned_documents):
    term = clean_special_characters(term).strip().lower()
    num_docs_with_term = sum(1 for doc in cleaned_documents if term in doc.lower())

    if num_docs_with_term > 0:
        log_result = 1 + math.log(
            len(cleaned_documents) / num_docs_with_term
        )  # 1 is added for smoothing
        return log_result
    else:
        return 0


def preprocess_document(document):
    terms_list = re.split(r"[,\s]+", document)
    cleaned_terms = [
        stemmer.stem(clean_special_characters(term).lower())
        for term in terms_list
        if term.lower() not in STOP_WORDS
    ]
    return cleaned_terms


def clean_documents(documents_dict):
    cleaned_documents = [
        " ".join(preprocess_document(doc)) for doc in documents_dict.values()
    ]
    return cleaned_documents


def generate_document_vector(document, vocabulary, cleaned_documents):
    terms_list = preprocess_document(document)
    tfidf_vector = np.zeros(len(vocabulary))
    term_freq = calculate_term_frequency(terms_list)

    for i, term in enumerate(vocabulary):
        term = clean_special_characters(term)
        if term in term_freq:
            tfidf_vector[i] = term_freq[term] * calculate_inverse_document_frequency(
                term, cleaned_documents
            )
    return tfidf_vector


def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vec1 = np.linalg.norm(vector1)
    norm_vec2 = np.linalg.norm(vector2)

    # Check for zero division
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    else:
        return dot_product / (norm_vec1 * norm_vec2)


def pearson_similarity(vector1, vector2):
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


def get_recommendations(search_history, documents, model="cosine"):
    cleaned_docs = clean_documents(documents)
    vocabulary = list(set([term for doc in cleaned_docs for term in doc.split()]))
    tfidf_matrix = []

    for key, doc in documents.items():
        tfidf_vector = generate_document_vector(doc, vocabulary, cleaned_docs)
        tfidf_matrix.append((key, tfidf_vector))

    search_tfidf = generate_document_vector(search_history, vocabulary, cleaned_docs)
    similarities = []
    for _, doc_tfidf in tfidf_matrix:
        if model == "cosine":
            similarities.append(cosine_similarity(search_tfidf, doc_tfidf))
        else:
            similarities.append(pearson_similarity(search_tfidf, doc_tfidf))

    sorted_indices = np.argsort(similarities)[::-1]

    recommendations = [(tfidf_matrix[i][0], similarities[i]) for i in sorted_indices]
    return recommendations

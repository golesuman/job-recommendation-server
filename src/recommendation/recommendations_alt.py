import math
import re
import numpy as np

STOP_WORDS = set(["the", "and", "is", "in", "it", "to", "of", "this", "that", "for"])


def remove_special_characters(word):
    pattern = r"[^\w\s]"
    cleaned_word = re.sub(pattern, "", word)
    return cleaned_word


def calculate_tf(terms):
    tf_dict = {}
    total_terms = len(terms)
    for term in terms:
        term = remove_special_characters(term)
        if term not in tf_dict:
            tf_dict[term] = 0
        tf_dict[term] += 1 / total_terms
    return tf_dict


def calculate_idf(term, cleaned_documents):
    term = remove_special_characters(term).strip().lower()
    num_documents_with_term = sum(
        1 for document in cleaned_documents if term in document.lower()
    )

    if num_documents_with_term > 0:
        log_result = 1 + math.log(
            len(cleaned_documents) / num_documents_with_term
        )  # 1 is added for smoothing
        return log_result
    else:
        return 0


def preprocess(document):
    terms = re.split(r"[,\s]+", document)
    cleaned_terms = [
        remove_special_characters(term).lower()
        for term in terms
        if term.lower() not in STOP_WORDS
    ]
    return cleaned_terms


def clean_documents(documents):
    cleaned_documents = [
        " ".join(preprocess(document)) for document in documents.values()
    ]
    return cleaned_documents


def fit_document(document, vocabulary, cleaned_documents):
    terms = preprocess(document)
    tf_idf_vector = np.zeros(len(vocabulary))
    tf = calculate_tf(terms)

    for i, term in enumerate(vocabulary):
        term = remove_special_characters(term)
        if term in tf:
            tf_idf_vector[i] = tf[term] * calculate_idf(term, cleaned_documents)
    return tf_idf_vector


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Check for zero division
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    else:
        return dot_product / (norm_vec1 * norm_vec2)


def pearson_similarity(vec1, vec2):
    mean_vec1 = np.mean(vec1)
    mean_vec2 = np.mean(vec2)

    # Compute Pearson correlation coefficient
    numerator = np.sum((vec1 - mean_vec1) * (vec2 - mean_vec2))
    denominator = np.sqrt(np.sum((vec1 - mean_vec1) ** 2)) * np.sqrt(
        np.sum((vec2 - mean_vec2) ** 2)
    )
    if denominator == 0:
        return 0.0
    else:
        return numerator / denominator


def get_recommendations(search_history, documents, model="cosine"):
    cleaned_documents = clean_documents(documents)
    vocabulary = list(
        set([term for document in cleaned_documents for term in document.split()])
    )
    tfidf_matrix = []

    for key, document in documents.items():
        tf_idf_vector = fit_document(document, vocabulary, cleaned_documents)
        tfidf_matrix.append((key, tf_idf_vector))

    search_tfidf = fit_document(search_history, vocabulary, cleaned_documents)
    similarities = []
    for _, doc_tfidf in tfidf_matrix:
        if model == "cosine":
            similarities.append(cosine_similarity(search_tfidf, doc_tfidf))
        else:
            similarities.append(pearson_similarity(search_tfidf, doc_tfidf))

    sorted_indices = np.argsort(similarities)[::-1]

    recommendations = [(tfidf_matrix[i][0], similarities[i]) for i in sorted_indices]
    return recommendations

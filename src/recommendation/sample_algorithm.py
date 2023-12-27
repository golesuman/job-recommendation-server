import math
from collections import defaultdict
# Sample documents
documents = {
    1: "backend, django, devops, python",
    2: "backend, python, senior ",
    3: "react, bootstrap, css, frontend, junior",
    4: "bootstrap, react, css, senior",
}


def preprocess(document):
    # Tokenization: Split the document into words (terms)
    terms = document.lower().split()
    return terms


def calculate_tf(terms):
    tf_dict = {}
    total_terms = len(terms)
    for term in terms:
        if term not in tf_dict:
            tf_dict[term] = 0
        tf_dict[term] += 1 / total_terms
    return tf_dict


def calculate_idf(documents, term):
    num_documents_with_term = sum(1 for document in documents if term in document)
    if num_documents_with_term > 0:
        return math.log(len(documents) / num_documents_with_term)
    else:
        return 0


def calculate_tfidf(documents):
    tfidf_matrix = []
    for key, document in documents.items():
        terms = preprocess(document)
        tf = calculate_tf(terms)
        tfidf_vector = [tf[term] * calculate_idf(list(documents.values()), term) for term in terms]
        tfidf_matrix.append((key, tfidf_vector))
    return tfidf_matrix


def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))


def magnitude(vector):
    return math.sqrt(sum(x**2 for x in vector))


def cosine_similarity(doc1, doc2):
    dot_product_value = dot_product(doc1, doc2)
    magnitude_doc1 = magnitude(doc1)
    magnitude_doc2 = magnitude(doc2)

    if magnitude_doc1 == 0 or magnitude_doc2 == 0:
        return 0  # To handle division by zero

    return dot_product_value / (magnitude_doc1 * magnitude_doc2)


tfidf_matrix = calculate_tfidf(documents)
print("the tf-idf matrix is")

print(tfidf_matrix)


print("doc1 and doc2 are:")
doc1 = tfidf_matrix[2]
doc2 = tfidf_matrix[3]
print(doc1, doc2)
similarities = defaultdict()
# print(" ")
print("The similarities are :")
for item, value in tfidf_matrix:
    # print(item, value)
# for i in range(1, len(tfidf_matrix)):
    similarity = cosine_similarity(tfidf_matrix[0][1], value)
    similarities[item] = similarity
    # print(similarity)

print(similarities)
print(sorted(similarities.items(), key=lambda x: x[1], reverse=True))

# Print the TF-IDF vectors
# for i, document in enumerate(documents):
#     print(f"Document {i + 1} - TF-IDF Vector: {tfidf_matrix[i]}")


# print(f"Cosine Similarity between Document 1 and Document 4: {similarity:.4f}")

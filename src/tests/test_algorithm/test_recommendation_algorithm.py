from math import ceil
import pytest
import numpy as np
from recommendation.algorithms_v2 import (
    remove_special_characters,
    calculate_tf,
    calculate_idf,
    preprocess,
    clean_documents,
    fit_document,
    cosine_similarity,
    pearson_similarity,
    get_recommendations,
)


def test_remove_special_characters():
    assert remove_special_characters("Hello! World.") == "Hello World"
    assert remove_special_characters("This is a test!") == "This is a test"


def test_calculate_tf():
    terms = ["hello", "world", "hello", "python", "world"]
    tf_dict = calculate_tf(terms)
    assert tf_dict == {"hello": 0.4, "world": 0.4, "python": 0.2}


# Test calculate_idf function
def test_calculate_idf():
    cleaned_documents = ["hello world", "world python", "python python"]
    assert calculate_idf("hello", cleaned_documents) == 2.09861228866811
    assert calculate_idf("world", cleaned_documents) == 1.4054651081081644
    assert calculate_idf("python", cleaned_documents) == 1.4054651081081644


# Test preprocess function
def test_preprocess():
    document = "Hello, world! This is a test."
    cleaned_terms = preprocess(document)
    assert cleaned_terms == ["hello", "world", "tes"]


# Test clean_documents function
def test_clean_documents():
    documents = {
        "doc1": "Hello, world!",
        "doc2": "Python is awesome.",
    }
    cleaned_documents = clean_documents(documents)
    assert cleaned_documents == ["hello world", "python awesom"]


def test_cosine_similarity():
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([2, 4, 6])
    assert cosine_similarity(vec1, vec2) == 1.0


def test_pearson_similarity():
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([2, 4, 6])
    assert ceil(pearson_similarity(vec1, vec2)) == 1.0

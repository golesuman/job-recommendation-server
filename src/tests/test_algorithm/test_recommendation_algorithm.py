import pytest
import numpy as np
from recommendation.algorithms_v2 import (
    PorterStemmer,
    TextAnalyzer,
)
import math


@pytest.fixture
def stemmer():
    return PorterStemmer()


@pytest.fixture
def analyzer():
    return TextAnalyzer()


def test_porter_stemmer_count_consonant_sequences(stemmer):
    assert stemmer.count_consonant_sequences("tr") == 1
    assert stemmer.count_consonant_sequences("o") == 0
    assert stemmer.count_consonant_sequences("trash") == 2


def test_porter_stemmer_contains_vowel(stemmer):
    assert stemmer.contains_vowel("hello") is True
    assert stemmer.contains_vowel("xyz") is False
    assert stemmer.contains_vowel("aeiou") is True


def test_text_analyzer_clean_special_characters(analyzer):
    assert analyzer.clean_special_characters("Hello!") == "Hello"
    assert analyzer.clean_special_characters("This is a test.") == "This is a test"


def test_text_analyzer_calculate_term_frequency(analyzer):
    terms_list = ["hello", "world", "hello", "python", "world"]
    tf_dict = analyzer.calculate_term_frequency(terms_list)
    assert tf_dict == {"hello": 0.4, "world": 0.4, "python": 0.2}


def test_text_analyzer_calculate_inverse_document_frequency(analyzer):
    analyzer.cleaned_documents = ["hell0", "world", "python", "python"]
    assert analyzer.calculate_inverse_document_frequency("hello") == 2.386294361119891
    assert analyzer.calculate_inverse_document_frequency("world") == 1.6931471805599454
    assert analyzer.calculate_inverse_document_frequency("python") == 1.2876820724517808


def test_text_analyzer_preprocess_document(analyzer):
    document = "Hello, world! This is a test."
    cleaned_terms = analyzer.preprocess_document(document)
    assert cleaned_terms == ["hello", "world", "test"]


def test_text_analyzer_clean_documents(analyzer):
    documents = {
        "doc1": "Hello, world!",
        "doc2": "Python is awesome.",
    }
    analyzer.clean_documents(documents)
    assert analyzer.cleaned_documents == ["hello world", "python awesome"]


def test_text_analyzer_cosine_similarity(analyzer):
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([2, 4, 6])
    assert analyzer.cosine_similarity(vec1, vec2) == 1.0


def test_text_analyzer_pearson_similarity(analyzer):
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([2, 4, 6])
    assert math.ceil(analyzer.pearson_similarity(vec1, vec2)) == 1.0


def test_text_analyzer_get_recommendations_cosine(analyzer):
    data = "Python programming is fun"
    documents = {
        "doc1": "Python programming is awesome",
        "doc2": "I love programming in Python",
    }
    recommendations = analyzer.get_recommendations(data, documents, model="cosine")
    assert recommendations[0][0] == "doc1"


def test_text_analyzer_get_recommendations_pearson(analyzer):
    data = "Python programming is fun"
    documents = {
        "doc1": "Python programming is awesome",
        "doc2": "I love programming in Python",
    }
    recommendations = analyzer.get_recommendations(data, documents, model="pearson")
    assert recommendations[0][0] == "doc1"

import re
from .constants import STOP_WORDS

REGEX_TO_REMOVE_SPECIAL_CHARACTERS = r"[^a-zA-Z0-9\s]"


class PreProcessing:
    def __init__(self, document):
        self.document = document

    def remove_stop_words(self):
        results = []
        for word in self.document:
            if word in STOP_WORDS:
                results.append(word)
        return results

    def remove_special_characters(self):
        cleaned_document = re.sub(REGEX_TO_REMOVE_SPECIAL_CHARACTERS, "", self.document)
        return cleaned_document


def remove_special_characters(word):
    cleaned_word = re.sub(r"[^a-zA-Z0-9\s]", "", word)
    return cleaned_word.lower()

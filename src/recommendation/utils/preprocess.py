import re
from .constants import STOP_WORDS

REGEX_TO_REMOVE_SPECIAL_CHARACTERS = r"[^a-zA-Z0-9\s]"


def remove_special_characters(word):
    cleaned_word = re.sub(r"[^a-zA-Z0-9\s]", "", word)
    return cleaned_word.lower()

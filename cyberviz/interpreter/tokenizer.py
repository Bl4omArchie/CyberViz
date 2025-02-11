import os
import re
import json


# Remove special caracters and lowercase headers
def tokenize_headers(columns: list) -> list:
    headers = [re.split(r'[\W_]+', header.lower().strip()) for header in columns]
    return headers


def get_lexicon(filepath: str) -> list:
    with open(filepath, 'r') as file:
        lexicon = json.load(file)

    return {synonym: key for key, synonyms in lexicon.items() for synonym in synonyms}
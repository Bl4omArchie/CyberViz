import json
import os
import re



# Remove special caracters and lowercase headers
def tokenize_headers(columns: list) -> list:
    headers = [re.split(r'[\W_]+', header.lower().strip()) for header in columns]
    return headers


def get_lexicon(filepath: str) -> list:
    with open(filepath, 'r') as file:
        lexicon = json.load(file)

    return {synonym: key for key, synonyms in lexicon.items() for synonym in synonyms}


def match_headers(lexicon_path: list, datasets: object) -> list:
    lex = get_lexicon(lexicon_path)
    matching_columns = []
    unmatching_columns = []

    for dataset in datasets:
        columns.append(tokenize_headers(dataset.get_columns()))

    return [matching_columns, unmatching_columns]
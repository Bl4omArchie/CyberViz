import json
import os
import re

# A lexicon is a set of synonym or abbreviation where one word is picked to represent all of them
# 
# Parameters :
#   filepath : the lexicon is a json file (see example in lexicon.json) 
#
def get_lexicon(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        lexicon = json.load(file)

    return {synonym: key for key, synonyms in lexicon.items() for synonym in synonyms}


# Remove special characters, lowercase headers, unified headers with lexicon
#
# Parameters :
#   set_headers : headers from a file
#
# Return :
#   The tokenized headers
#
def tokenize_headers(set_headers: list, lexicon: dict) -> list:
    tokenized_headers = []

    for header in set_headers:
        tokens = re.split(r'[\W_]+', header.lower().strip())     # Remove special characters and lowercase
        unified_tokens = [lexicon.get(token, token) for token in tokens]    # Use lexicon to unify words and abbreviations
        tokenized_headers.append(unified_tokens)

    return tokenized_headers


# Take two sets of headers and match them into one set
def match_headers(headers_a: list, headers_b: list, lexicon: dict) -> list:
    tokenized_headers_a = tokenize_headers(headers_a, lexicon)
    tokenized_headers_b = tokenize_headers(headers_b, lexicon)

    set_merged_headers = []
    unmatched_headers = []

    for header_a in tokenized_headers_a:
        if header_a in tokenized_headers_b:
            set_merged_headers.append(header_a)
        else:
            unmatched_headers.append(header_a)

    for header_b in tokenized_headers_b:
        if header_b not in tokenized_headers_a:
            unmatched_headers.append(header_b)

    return [set_merged_headers, unmatched_headers]
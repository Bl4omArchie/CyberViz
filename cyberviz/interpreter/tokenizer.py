import Levenshtein
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

    #TODO : translate into english, correct grammar errors

    for header in set_headers:
        tokens = re.split(r'[\W_]+', header.lower().strip())                # Remove special characters and lowercase
        unified_tokens = [lexicon.get(token, token) for token in tokens]    # Use lexicon to unify words and abbreviations
        tokenized_headers.append("".join(unified_tokens))                   # Join tokens without spaces

    return tokenized_headers


# Match headers from two different set
#
# Parameters :
#   headers_a : headers base comparison
#   headers_b : headers to be compared to headers_a
#   lexicon : the reversed lexicon ( use get_lexicon() )
#
# Return :
#   A dict with each headers_b as a key add with the matching header_a as a value
#   If no headers match, the value is None
# 
def match_headers(headers_a: list, headers_b: list, lexicon: dict) -> dict:
    res = {}
    tha = tokenize_headers(headers_a, lexicon)
    thb = tokenize_headers(headers_b, lexicon)

    #TODO : more flexible matching. For instance fl4w_duration should match flow_duration

    for hb, tokenized_hb in zip(headers_b, thb):
        match = None
        for ha, tokenized_ha in zip(headers_a, tha):
            if tokenized_hb == tokenized_ha:
                match = ha
                break
        res[hb] = match

    return res


# Format headers to a specific correction : english, lowercase, grammar check, spaced with underscore
#
# Parameters :
#   headers_a : a list of headers to be corrected
#   lexicon : your lexicon for unification of synonym and abreviation
#
def correct_headers(headers_a: list, lexicon: dict) -> list:
    res = []

    return res
from pathlib import Path

import json
import os
import re



# The tokenize is a class to correct and tokenize headers
# A lexicon is a set of synonym or abbreviation where one word is picked to represent all of them
#
# Parameter :
#   lexicon_path : path to your lexicon (json file)   
#
class Tokenizer:
    def __init__(self, lexicon_path: str):
        self.lexicon_path = Path(lexicon_path)

        if not self.lexicon_path.is_file():
            raise ValueError("[!] Invalid lexicon path")

        self.reverse_lexicon = None

    
    # Algorithm : A reversed lexicon is an reversed dictionnary which make search function fast as O(1).  
    #
    # Complexity :
    #   Search : O(1)
    def get_reverse_lexicon(self):
        with open(self.lexicon_path, 'r') as file:
            self.reverse_lexicon = json.load(file)

        self.reverse_lexicon = {synonym: key for key, synonyms in self.reverse_lexicon.items() for synonym in synonyms}


    # Feature : Remove special characters, lowercase headers, unified words with lexicon
    #
    # Parameters :
    #   set_headers : headers from a file
    #
    # Return :
    #   The tokenized headers
    #
    def tokenize_headers(self, set_headers: list) -> list:
        tokenized_headers = []

        #TODO : translate into english, correct grammar errors

        for header in set_headers:
            header_token = header.replace(" ", "_").replace(".", "_").lower().split("_")

            for i in range(len(header_token)):
                word = self.reverse_lexicon.get(header_token[i])
                if word is not None:
                    header_token[i] = word
            tokenized_headers.append("_".join(header_token))

        return tokenized_headers
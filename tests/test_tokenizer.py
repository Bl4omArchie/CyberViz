from cyberviz.interpreter.tokenizer import *

import unittest
import json



class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.lexicon_path = "cyberviz/interpreter/lexicon.json"
        self.lexicon = get_lexicon(self.lexicon_path)
    

    def test_match_headers(self):
        headers1 = ['header1', 'header2', 'header54']
        headers2 = ['header2', 'header3']
        expected_result = ['header1', 'header2', 'header54', 'header3']

        result = match_headers(headers1, headers2, get_lexicon(self.lexicon_path))
        self.assertEqual(result, expected_result)

    def test_tokenize_headers(self):
        headers = ['Header1!', 'HEADER2@', 'header3#']
        expected_result = ['header1', 'header2', 'header3']
        
        result = tokenize_headers(headers, self.lexicon)
        self.assertEqual(result, expected_result)
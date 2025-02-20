from cyberviz.interpreter.tokenizer import *

import unittest
import json


test_csv1 = """flow_totAL,flow_partial@,label,test_column4
0,0.4656,0.353, Attack, truc
1,0.4656,0.353, Attack, hiboux
2,0.9986,0.153, Attack, chouette
5,0.7656,0.9, Benign, eve
6,0.6456,0.33, Benign, alice
""" 


header_test_one = ["avg.flow_duration", "win_size78_@", "average_tcp_flow"]
header_test_two = ["average-flow-time", "window_size", "avg_flow"]

expected_match_header_two = {"average-flow-time": "avg.flow_duration", "window_size": "win_size78_@", "avg_flow": None}
expected_corr_header_one = ["average_flow_duration", "win_size_78_@", "average_tcp_flow"]
expected_corr_header_two = ["average_flow_duration", "window_size", "average_flow"]


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.lexicon_path = "cyberviz/interpreter/lexicon.json"
        self.lexicon = get_lexicon(self.lexicon_path)
    

    def test_match_headers(self):
        headers1 = ["header1", "average", "window_size"]
        headers2 = ["avg", "win_size"]
        expected_result = {"avg": "average", "win_size": None}

        result = match_headers(headers1, headers2, get_lexicon(self.lexicon_path))
        self.assertEqual(result, expected_result)

    def test_tokenize_headers(self):
        headers = ["Header1!", "HEADER2@", "header3#"]
        expected_result = ["header1", "header2", "header3"]
        
        result = tokenize_headers(headers, self.lexicon)
        self.assertEqual(result, expected_result)
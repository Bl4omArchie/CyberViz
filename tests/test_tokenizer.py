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



# TODO : there is still a lot of cases where the algorithm doesn't work (ie: with number or separated words)
class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.lexicon_path = "cyberviz/interpreter/lexicon.json"
               
        self.header_test_one = ["avg.flow_duration", "bwd_78_@", "average_tcp_flow"]
        self.expected_tokenized_header_one = ["average_flow_duration", "backward_78_@", "average_tcp_flow"]

        self.tokenizer = Tokenizer(self.lexicon_path)
        self.tokenizer.get_reverse_lexicon()

    def test_tokenize_headers(self):
        print (self.tokenizer.tokenize_headers(self.header_test_one))
        self.assertEqual(self.tokenizer.tokenize_headers(self.header_test_one), self.expected_tokenized_header_one)
            
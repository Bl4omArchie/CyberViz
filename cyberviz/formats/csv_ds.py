from cyberviz.dataset import Dataset
from cyberviz.interpreter.tokenizer import * 

import dask.dataframe as dd
import pandas as pd
import Levenshtein


class CsvDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".csv":
            raise ValueError("[!] CSV file only")
        else:
            self.format_dataset = "csv"
            self.extension_dataset = ".csv"

        self.parameters = {
            "sep":None,             # separator between each values
            "blocksize":None,       # number of bytes by which to cut up larger files
            "chunksize":None,       # number of rows to include in each chunk
            "usecols":None,         # specify which columns you want to use
            "engine": "pyarrow",    # engine to use for parsing (ie : pyarrow, c)
            "assume_missing":False, # if True, all integer columns that aren’t specified in dtype are assumed to contain missing values, and are converted to floats
            "nrows":None,           # number of rows to read at a time
            "encoding":"UTF-8",     # encoding of the file
            "extra_parameters":None # extra parameters
        }

        self.lexicon_path = "cyberviz/interpreter/lexicon.json"
        
        # When the levenshtein ration is above 0.8, the two compared string are most likely the same (ie : column and column8 are the same)
        self.levenshtein_ratio_min = 0.8


    # Requirements : When the dataset is active, data is loaded into memory
    #
    # Arguments :
    #   chunksize=None : you can split your csv into several files to avoid memory overflow
    #   usecols=None : specify which columns you want to use
    #   sep=None : specify the seperator used by your CSV
    #   encoding="UTF-8 : default encoding is UTF-8
    def activate_dataset(self, **kwargs):
        input_set = set(kwargs.keys())
        
        for input in input_set:
            if input not in self.parameters.keys():
                self.parameters["extra_parameters"] = kwargs[input]
            self.parameters[input] = kwargs[input]
        
        self.open_dataset()
        self.status = True
        
    
    # Requirements : Load the csv dataset into memory
    #
    # Parameters :
    #   chunksize : split the csv into multiple file so you don't open it all
    #   usecols : specificy columns from your dataset
    #   sep : define the separator
    #   encoding : UTF-8 by default
    #
    def open_dataset(self):
        read_csv_params = {key: value for key, value in self.parameters.items() if value is not None}
        self.data = dd.read_csv(self.path_dataset, **read_csv_params)


    # Feature : Merge two csv into one by correlating columns
    #
    # Parameters:
    #   lexicon_path : a lexicon is a set of synonym or abreviation where one word is picked to represent all of them
    #   dataset : the dataset to merge with
    #
    # Warnings:
    #   Merging two csv is relevant only if both csv means the same thing. 
    #   If both have similar columns but different meaning, your work on them will not be relevant 
    #
    def merge_headers(self, dataset: object):
        if self.status == False or dataset.status == False:
            raise ValueError("[!] Datasets are inactive. Please activate them first.")

        tokener = Tokenizer(self.lexicon_path)
        tokener.get_reverse_lexicon()
        tokened_a = tokener.tokenize_headers(self.data.columns.tolist())
        tokened_b = tokener.tokenize_headers(dataset.data.columns.tolist())

        matching_headers = {}

        for i in range(len(tokened_a)):
            for y in range(len(tokened_b)):
                if Levenshtein.ratio(tokened_a[i], tokened_b[y]) > 0.8:
                    matching_headers[tokened_b[i]: tokened_a[i]]

        # TODO : handle merging of the two datasets


        """
        for header_b, value in merged_headers.items():
            if value is not None:
                self.data = self.data.merge(dataset.data[[header_b]], left_on=value, right_on=header_b, how='left')
        
        self.data.to_csv(self.path_dataset, single_file=True)
        """

    # Feature : use the same logic for merging two datasets but instead modify the current dataset headers for more standard headers
    #
    def correct_headers(self):
        if self.status == False:
            raise ValueError("[!] Datasets are inactive. Please activate them first.")


    # Requirements : set the lexicon path (json file)
    def set_lexicon_path(self, lexicon_path: str):
        self.lexicon_path = lexicon_path 


    def get_headers(self):
        if self.status:
            return self.data.columns.tolist()
        else:
            raise ValueError("[!] Dataset is inactive. Please activate the dataset first.")


    def basics_data(self):
        if self.status == False:
            raise ValueError("[!] Dataset is inactive. Please activate it first.")

        # Count the number of 'Label' values that are True
        true_label_count = self.data[self.data['Label'] == True].shape[0].compute()
        print(true_label_count)
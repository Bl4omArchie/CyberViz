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
            "sep":None,
            "blocksize":None,
            "chunksize":None,
            "usecols":None,
            "engine": "pyarrow",
            "assume_missing":False,
            "nrows":None,
            "encoding":"UTF-8",
            "extra_parameters":None
        }

        self.lexicon_path = "cyberviz/interpreter/lexicon.json"
        self.levenshtein_ratio_min = 0.8

    def activate_dataset(self, **kwargs):
        """
        When the dataset is active, data is loaded into memory

        Arguments:
            chunksize=None: you can split your csv into several files to avoid memory overflow
            usecols=None: specify which columns you want to use
            sep=None: specify the separator used by your CSV
            encoding="UTF-8": default encoding is UTF-8
        """
        input_set = set(kwargs.keys())
        
        for input in input_set:
            if input not in self.parameters.keys():
                self.parameters["extra_parameters"] = kwargs[input]
            self.parameters[input] = kwargs[input]
        
        self.open_dataset()
        self.status = True
        
    def open_dataset(self):
        """
        Load the csv dataset into memory

        Parameters:
            chunksize: split the csv into multiple file so you don't open it all
            usecols: specify columns from your dataset
            sep: define the separator
            encoding: UTF-8 by default
        """
        read_csv_params = {key: value for key, value in self.parameters.items() if value is not None}
        self.data = dd.read_csv(self.path_dataset, **read_csv_params)

    def merge_headers(self, dataset: object):
        """
        Merge two csv into one by correlating columns

        Parameters:
            lexicon_path: a lexicon is a set of synonym or abbreviation where one word is picked to represent all of them
            dataset: the dataset to merge with

        Warnings:
            Merging two csv is relevant only if both csv means the same thing.
            If both have similar columns but different meaning, your work on them will not be relevant
        """
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

        # TODO: handle merging of the two datasets

    def correct_headers(self):
        """
        Use the same logic for merging two datasets but instead modify the current dataset headers for more standard headers
        """
        if self.status == False:
            raise ValueError("[!] Datasets are inactive. Please activate them first.")

    def set_lexicon_path(self, lexicon_path: str):
        """
        Set the lexicon path (json file)
        """
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

    def analyze_csv(self):        
        columns = self.data.columns.tolist()
        file_size = self.data.memory_usage(deep=True).sum()
        num_rows, num_columns = self.data.shape
        
        stats = self.data.describe(include='all').to_dict()
        missing_values = self.data.isnull().sum().to_dict()
        
        return {
            'file_size': file_size,
            'num_rows': num_rows,
            'num_columns': num_columns,
        }

    # Convert a file to parquet format
    # Parameter :
    #   export_path: folder where your file will be converted
    #
    def export_to_parquet(self, export_path: str):
        export_dir = Path(export_path)
        export_dir.mkdir(parents=True, exist_ok=True)
        self.data.to_parquet(export_dir / file.stem, engine="pyarrow")


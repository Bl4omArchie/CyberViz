from cyberviz.dataset import Dataset
from cyberviz.interpreter.tokenizer import * 

import dask.dataframe as dd
import pandas as pd


class CsvDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".csv":
            raise ValueError("[!] CSV file only")
        else:
            self.format_dataset = "csv"
            self.extension_dataset = ".csv"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")

        self.parameters = (chunksize:=None, usecols:=None, sep:=None, encoding:="UTF-8")


    # When the dataset is active, data is loaded into memory
    # TODO : handle arguments checking
    #
    # Arguments :
    #   chunksize=None : you can split your csv into several files to avoid memory overflow
    #   usecols=None : specify which columns you want to use
    #   sep=None : specify the seperator used by your CSV
    #   encoding="UTF-8 : default encoding is UTF-8
    def activate_dataset(self, **kwargs):
        input_set = set(kwargs.keys())
        args_set = ("chunksize", "usecols", "sep", "encoding")

        self.open_dataset()

        self.status = True
        
    
    # Load the csv dataset into memory
    #
    # Parameters :
    #   chunksize : split the csv into multiple file so you don't open it all
    #   usecols : specificy columns from your dataset
    #   sep : define the separator
    #   encoding : UTF-8 by default
    #
    def open_dataset(self):
        if self.parameters.chunksize:
            self.data = dd.read_csv(self.path_dataset, chunksize=self.parameters.chunksize, usecols=self.parameters.usecols, sep=self.parameters.sep, encoding=self.parameters.encoding)
            self.data = self.data[0]
        else:
            self.data = dd.read_csv(self.path_dataset, usecols=self.parameters.usecols, sep=self.parameters.sep, encoding=self.parameters.encoding)


    # Correlate columns from different csv
    #
    # Parameters:
    #   lexicon_path : a lexicon is a json with several words for one translation
    #   dataset : another csv so you can merge them
    #
    # Warnings:
    #   Merging two csv is relevant only if both csv means the same thing. 
    #   If both have similar columns but different meaning, your work on them will not be relevant 
    def merge_dataset(self, lexicon_path: str, dataset: object) -> object:
        if self.status == False | dataset.status == False:
            raise ValueError("[!] Dataset are inactive. Please activate them first.")

        lex = get_lexicon(lexicon_path)

        columns1 = self.get_columns()
        columns2 = dataset.get_columns()
        
        th1 = tokenize_headers(columns1)
        th2 = tokenize_headers(columns2)


    def get_columns(self):
        if self.status:
            return self.data.columns.tolist()
        else:
            raise ValueError("[!] Dataset is inactive. Please activate the dataset first.")


    def basics_data(self):
        pass
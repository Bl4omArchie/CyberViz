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


    # When the dataset is active, data is loaded into memory
    def activate_dataset(self, chunksize=None, usecols=None, sep=None, encoding="UTF-8"):
        self.status = True
        self.open_dataset(chunksize, usecols, sep, encoding)
        
    
    # Load the csv dataset into memory
    #
    # Parameters :
    #   chunksize : split the csv into multiple file so you don't open it all
    #   usecols : specificy columns from your dataset
    #   sep : define the separator
    #   encoding : UTF-8 by default
    #
    def open_dataset(self, chunksize=None, usecols=None, sep=None, encoding="UTF-8"):
        if chunksize:
            self.data = dd.read_csv(self.path_dataset, chunksize=chunksize, usecols=usecols, sep=sep, encoding=encoding)
            self.data = self.data[0]
        else:
            self.data = dd.read_csv(self.path_dataset, usecols=usecols, sep=sep, encoding=encoding)


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
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

        self.parameters = {
            "sep":None,             # separator between each values
            "blocksize":None,       # number of bytes by which to cut up larger files
            "chunksize":None,       # number of rows to include in each chunk
            "usecols":None,         # specify which columns you want to use
            "engine": "pyarrow",     # engine to use for parsing (ie : pyarrow, c)
            "assume_missing":False, # if True, all integer columns that aren’t specified in dtype are assumed to contain missing values, and are converted to floats
            "nrows":None,           # number of rows to read at a time
            "encoding":"UTF-8",     # encoding of the file
            "extra_parameters":None # extra parameters
        }


    # When the dataset is active, data is loaded into memory
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
        
    
    # Load the csv dataset into memory
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
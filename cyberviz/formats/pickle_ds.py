from cyberviz.dataset import Dataset
from cyberviz.interpreter.tokenizer import * 

import dask.dataframe as dd
import pandas as pd
import sklearn
import pickle


class PickleDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".pickle":
            raise ValueError("[!] Pickle file only")
        else:
            self.format_dataset = "pickle"
            self.extension_dataset = ".pickle"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")

    def activate_dataset(self):
        """
        When the dataset is active, data is loaded into memory
        """
        self.status = True
        self.open_dataset()
        
    def open_dataset(self):
        """
        Load the pickle dataset into memory
        """
        dbfile = open(self.path_dataset, 'rb')
        self.data = pickle.load(dbfile)
        self.status = True
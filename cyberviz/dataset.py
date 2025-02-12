from cyberviz.interpreter.tokenizer import *
from cyberviz.convert import export
from cyberviz.plot import analyze
from pathlib import Path

import dask.dataframe as dd
import pandas as pd
import hashlib
import h5py




class Dataset:
    def __init__(self, path: str):
        self.dsid = self.compute_hash_dataset(path)
        self.data = None
        self.path_dataset = Path(path)
        self.format_dataset = None
        self.extension_dataset = None
        self.activity = False


    # Hash the files as the dataset id (dsid)
    # 
    # Parameter :
    #   path : path to your dataset
    #
    def compute_hash_dataset(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    # Compare the hash of two dataset
    #
    # Return :
    #   boolean : true or false
    def compare(self, dataset: object) -> bool:
        return self.dsid == self.compute_hash_dataset(dataset.path)

    # Free the memory
    def stop(self):
        self.status = false
        self.data = None

    def get(self):
        return self


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
    def activate(self, chunksize=None, usecols=None, sep=None, encoding="UTF-8"):
        self.status = True
        self.open_dataset(chunksize, usecols, sep, encoding)
        
    
    # Load the dataset into memory with data var
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
    def merge_csv(self, lexicon_path: str, dataset: object):
        if self.status == False | dataset.status == False:
            raise ValueError("[!] Dataset are inactive. Please activate them first.")

        lex = get_lexicon(lexicon_path)

        columns1 = self.get_columns()
        columns2 = dataset.get_columns()
        
        th1 = tokenize_headers(columns1)
        th2 = tokenize_headers(columns2)

        print (lex)


    def get_columns(self):
        if self.status:
            return self.data.columns.tolist()
        else:
            raise ValueError("[!] Dataset is inactive. Please activate the dataset first.")


    def basics_data(self):
        pass
        
     
class PcapDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".pcap":
            raise ValueError("[!] PCAP file only")
        else:
            self.format_dataset = "pcap"
            self.extension_dataset = ".pcap"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")
        
        
class ParquetDataset(Dataset):
    def __init__(self, folderpath: str, file_cursor: str="part.0.parquet"):
        super().__init__(folderpath)
        
        self.format_dataset = ".parquet"
        self.extension_dataset = [".parquet", ".pq", ".parq"]
        self.file_cursor = file_cursor
                
    def compute_hash_dataset(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()

    def open_dataset(self):
        self.data = dd.read_parquet(self.file_cursor, 'r')
        

class Hdf5Dataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".h5":
            raise ValueError("[!] HDF5 file only")
        else:
            self.format_dataset = "hdf5"
            self.extension_dataset = ".h5"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")
        
    def open_dataset(self):
        self.data = h5py.File(self.path_dataset, 'r')
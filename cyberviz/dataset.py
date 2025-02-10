from pathlib import Path
from cyberviz import analyze
from cyberviz import export
import pandas as pd

import hashlib
import random



class Dataset:
    def __init__(self, dsid: int):  
        self.dsid = dsid
        self.dataframe = None
        self.path_dataset = None
        self.hash_dataset = None
        self.format_dataset = None
        self.extension_dataset = None
        
    def compute_hash_dataset(self, filepath: str):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def compare(self, dataset: object):
        return self.hash_dataset == self.compute_hash_dataset(dataset.filepath)
    


class CsvDataset(Dataset):
    def __init__(self, dsid: int, filepath: str):
        super().__init__(dsid)
        
        test_filepath = Path(filepath)
        if test_filepath.suffix != ".csv":
            raise ValueError("[!] CSV file only")
        else:
            self.format_dataset = "csv"
            self.extension_dataset = ".csv"

        if not test_filepath.is_file():
            raise ValueError("[!] Invalid filepath")
        
        self.path_dataset = test_filepath
        self.hash_dataset = self.compute_hash_dataset(filepath)
        
    def open(self, chunksize=None, usecols=None, sep=None, encoding="UTF-8"):
        if chunksize:
            self.dataframe = pd.read_csv(self.path_dataset, chunksize=chunksize, usecols=usecols, sep=sep, encoding=encoding)
            for chunk in self.dataframe:
                pass
        else:
            self.dataframe = pd.read_csv(self.path_dataset, usecols=usecols, sep=sep, encoding=encoding)
            pass
        
    def basics_data(self):
        print (analyze.analyze_csv(self))
        
     
        
class PcapDataset(Dataset):
    def __init__(self, dsid: int, filepath: str):
        super().__init__(dsid)
        
        test_filepath = Path(filepath)
        if test_filepath.suffix != ".pcap":
            raise ValueError("[!] PCAP file only")
        else:
            self.format_dataset = "pcap"
            self.extension_dataset = ".pcap"

        if not test_filepath.is_file():
            raise ValueError("[!] Invalid filepath")
        
        self.path_dataset = test_filepath
        self.hash_dataset = self.compute_hash_dataset(filepath)
        
        
class ParquetDataset(Dataset):
    def __init__(self, dsid: int, folderpath: str, file_cursor: str="part.0.parquet"):
        super().__init__(dsid)
        
        self.path_dataset = folderpath
        self.format_dataset = ".parquet"
        self.extension_dataset = [".parquet", ".pq", ".parq"]
        self.file_cursor = file_cursor
                
    def compute_hash_dataset(self, filepath: str):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
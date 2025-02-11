from cyberviz.convert import export
from cyberviz.plot import analyze
from pathlib import Path
import dask.dataframe as dd
import h5py

import hashlib



class Dataset:
    def __init__(self, path: str):  
        self.dsid = self.compute_hash_dataset(path)
        self.dataframe = None
        self.path_dataset = Path(path)
        self.hash_dataset = self.dsid
        self.format_dataset = None
        self.extension_dataset = None
        
    def compute_hash_dataset(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def compare(self, dataset: object) -> bool:
        return self.hash_dataset == self.compute_hash_dataset(dataset.path)


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
        
    def open_dataset(self, chunksize=None, usecols=None, sep=None, encoding="UTF-8"):
        if chunksize:
            self.dataframe = dd.read_csv(self.path_dataset, chunksize=chunksize, usecols=usecols, sep=sep, encoding=encoding)
            for chunk in self.dataframe:
                pass
        else:
            self.dataframe = dd.read_csv(self.path_dataset, usecols=usecols, sep=sep, encoding=encoding)
            pass
        
    def basics_data(self):
        print (analyze.analyze_csv(self))
        
     
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
        self.dataframe = dd.read_parquet(self.file_cursor, 'r')
        

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
        self.dataframe = h5py.File(self.path_dataset, 'r')
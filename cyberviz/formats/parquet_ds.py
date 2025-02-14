from cyberviz.dataset import Dataset

import dask.dataframe as dd
import pandas as pd

class ParquetDataset(Dataset):
    def __init__(self, folderpath: str, file_cursor: str="part.0.parquet"):
        super().__init__(folderpath)
        
        self.format_dataset = ".parquet"
        self.extension_dataset = [".parquet", ".pq", ".parq"]
        self.file_cursor = file_cursor
                
    def hash_dataset(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()

    def open_dataset(self):
        self.data = dd.read_parquet(self.file_cursor, 'r')
from cyberviz.interpreter.tokenizer import *
from cyberviz.convert import export
from cyberviz.plot import analyze

from pathlib import Path
import hashlib


# Generic class
class Dataset:
    def __init__(self, path: str):
        self.path_dataset = Path(path)
        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")

        self.dsid = self.hash_dataset(path)
        self.data = None
        self.format_dataset = None
        self.extension_dataset = None
        self.status = False

    @staticmethod
    def hash_dataset(path: str) -> str:
        """
        Hash the files as the dataset id (dsid)

        Parameter:
            path: path to your dataset
        """
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def compare_dataset(self, dataset: object) -> bool:
        """
        Compare the hash of two datasets

        Return:
            boolean: true or false
        """
        return self.dsid == dataset.dsid

    def stop_dataset(self):
        """
        Free the memory
        """
        self.status = False
        self.data = None

    def get_dataset(self):
        return self
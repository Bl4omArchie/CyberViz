from cyberviz.interpreter.tokenizer import *
from cyberviz.convert import export
from cyberviz.plot import analyze

from pathlib import Path
import hashlib


class Dataset:
    def __init__(self, path: str):
        self.dsid = self.hash_dataset(path)
        self.data = None
        self.path_dataset = Path(path)
        self.format_dataset = None
        self.extension_dataset = None
        self.status = False


    # Hash the files as the dataset id (dsid)
    # 
    # Parameter :
    #   path : path to your dataset
    #
    def hash_dataset(self, path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    # Compare the hash of two datasets
    #
    # Return :
    #   boolean : true or false
    def compare_dataset(self, dataset: object) -> bool:
        return self.dsid == dataset.dsid

    # Free the memory
    def stop_dataset(self):
        self.status = False
        self.data = None

    def get_dataset(self):
        return self
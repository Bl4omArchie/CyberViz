from dataclasses import dataclass
from pathlib import Path

import hashlib
import json
import os


"""
Dataset is a python dataclass which is the generic representation of file containing data.

CsvFormat, ParquetFormat and PcapFormat are a higher level class for representing a collection of each types (pcap, csv and parquet).

The cyber-framework is handling those collections.
"""


@dataclass
class Dataset:
    name: str
    path: str
    dhash: str
    extension: str
    size: float
    data: bytes


def create_dataset(path: str) -> Dataset:
    path = Path(path)
    if not path.is_file():
        raise ValueError("[!] Invalid path")
    
    name = path.name
    dhash = compute_hash(path)
    ext = path.suffix
    size = path.stat().st_size / 1024 / 1024

    return Dataset(name=name, path=path, dhash=dhash, extension=ext, size=size, data=b"")


def compute_hash(path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


class CsvFormat:
    def __init__(self, dataset: Dataset):
        self.parameters = {
            "sep": None,
            "blocksize": None,
            "chunksize": None,
            "usecols": None,
            "engine": "pyarrow",
            "assume_missing": False,
            "nrows": None,
            "encoding": "UTF-8",
            "extra_parameters": None
        }

        self.dataset = dataset


    def export_to_parquet(self, export_path: str):
        export_dir = Path(export_path)
        export_dir.mkdir(parents=True, exist_ok=True)
        self.data.to_parquet(export_dir / file.stem, engine="pyarrow")


    def analyze_csv(self):        
        columns = self.data.columns.tolist()
        file_size = self.data.memory_usage(deep=True).sum()
        num_rows, num_columns = self.data.shape
        
        stats = self.data.describe(include='all').to_dict()
        missing_values = self.data.isnull().sum().to_dict()
        
        return {
            'file_size': file_size,
            'num_rows': num_rows,
            'num_columns': num_columns,
        }


class ParquetFormat:
    def __init__(self, parquet_files: list = None):
        self.parameters = {
            "engine": "pyarrow",
            "use_threads": True,
            "columns": None,
            "filters": None,
            "extra_parameters": None,
        }

        self.files = parquet_files


class PcapFormat:
    def __init__(self, pcap_files: list = None):
        self.parameters = {
            "snaplen": 65535,
            "promisc": True,
            "timeout": 1000,
            "extra_parameters": None,
        }

        self.files = pcap_files

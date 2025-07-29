from json import load
from cyberviz.dataset import Dataset

from abc import ABC, abstractmethod
from scapy.all import rdpcap
import dask.dataframe as dd
import streamlit as st


@st.cache_data
def load_cache_csv(path: str):
    return dd.read_csv(path, blocksize="16MB")


class BaseDataset(ABC):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.content = None
    
    @abstractmethod
    def preview(self, n=5):
        """Return a preview (head) of the dataset"""
        pass
    
    @abstractmethod
    def metadata(self):
        """Return useful metadata (columns, types, size, etc.)"""
        pass


class CsvDataset(BaseDataset):
    def __init__(self, dataset):
        super().__init__(dataset)
        if dataset.extension != "csv":
            raise ValueError(f"Incorrect type. You can't load a {dataset.extension} file into a CsvDataset.")
        
        self.content = load_cache_csv(self.dataset.path)

    def preview(self, n=5):
        return self.content.head(n)

    def metadata(self):
        if self.df is None:
            self.load()
        return {
            "columns": self.df.columns.tolist(),
            "dtypes": self.df.dtypes.compute().to_dict(),
            "n_rows": self.df.shape[0].compute(),
            "size_mb": self.size
        }


class PcapDataset(BaseDataset):
    def __init__(self, dataset):
        super().__init__(dataset)
        if dataset.extension != ".pcap":
            raise ValueError(f"Incorrect type. You can't load a {dataset.extension} file into a PcapDataset.")

        self.content = rdpcap(self.dataset.path)

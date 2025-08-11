from cyberviz.hash import compute_hash, compute_hash_from_bytes

from streamlit.runtime.uploaded_file_manager import UploadedFile
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from scapy.all import rdpcap
from pathlib import Path

import dask.dataframe as dd
import streamlit as st
import tempfile
import logging


@st.cache_data
def load_cache_csv(path: str):
    return dd.read_csv(path, blocksize="16MB")


class BaseDataset(ABC):
    def __init__(self, name: str, path: str, size: float, extension: str, dhash: str):
        self.name=name
        self.path=path
        self.size=size
        self.extension=extension
        self.dhash=dhash

    @classmethod
    def new_dataset(cls, path: str) -> "BaseDataset":
        file_path = Path(path)
        if not file_path.is_file():
            logging.warning(f"[!] Path {path} is not a valid file.")
            return None
        
        size_mb = file_path.stat().st_size / (1024 * 1024)
        return cls(
            name=file_path.name,
            path=str(file_path),
            size=round(size_mb, 3),
            extension=file_path.suffix.lower().lstrip("."),
            dhash=compute_hash(path)
        )
    
    @classmethod
    def upload_dataset(cls, dataset: UploadedFile) -> "BaseDataset":
        try:
            data_bytes = dataset.getvalue()
            size_mb = len(data_bytes) / (1024 * 1024)
            extension = Path(dataset.name).suffix.lower().lstrip(".")
        except Exception as e:
            logging.warning(f"Unable to get metadata : {e}")
            return None

        try:
            suffix = f".{extension}" if extension else ""
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp_file.write(data_bytes)
            tmp_file.flush()
            tmp_file.close()
        except Exception as e:
            logging.warning(f"Unable to upload the file : {e}")
            return None

        return cls(
            name=dataset.name,
            path=tmp_file.name,
            size=round(size_mb, 3),
            extension=extension,
            dhash=compute_hash_from_bytes(data_bytes)
        )
    
    @abstractmethod
    def preview(self, n=5):
        """Return a preview (head) of the dataset"""
        pass
    
    @abstractmethod
    def metadata(self):
        """Return useful metadata (columns, types, size, etc.)"""
        pass


class CsvDataset(BaseDataset):
    def __init__(self, name: str, path: str, size: float, extension: str, dhash: str):
        if extension != "csv":
            raise ValueError(f"Incorrect type. You can't load a {extension} file into a CsvDataset.")
        
        super().__init__(name, path, size, extension, dhash)
        self.content = load_cache_csv(self.path)


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


    def category(self, name: str):
        return self.content[name]


class PcapDataset(BaseDataset):
    def __init__(self, name: str, path: str, size: float, extension: str, dhash: str):
        if extension != "pcap":
            raise ValueError(f"Incorrect type. You can't load a {extension} file into a PcapDataset.")
        
        super().__init__(name, path, size, extension, dhash)
        self.content = rdpcap(self.path)


    def preview(self, n=5):
        return self.content[:n]


    def metadata(self):
        total_packets = len(self.content)
        protocols = set()
        packet_lengths = []

        for pkt in self.content:
            if hasattr(pkt, "proto"):
                protocols.add(pkt.proto)
            elif pkt.haslayer("IP"):
                protocols.add(pkt["IP"].proto)
            packet_lengths.append(len(pkt))

        return {
            "total_packets": total_packets,
            "unique_protocols": list(protocols),
            "average_packet_size": sum(packet_lengths) / total_packets if total_packets else 0,
            "min_packet_size": min(packet_lengths) if packet_lengths else 0,
            "max_packet_size": max(packet_lengths) if packet_lengths else 0
        }



@dataclass
class CollectionDataset:
    count: int = 0
    size: float = 0.0
    index: dict[str, BaseDataset] = field(default_factory=dict)

    @staticmethod
    def new_collection() -> "CollectionDataset":
        return CollectionDataset()

    def add_item(self, dataset: BaseDataset):
        self.index[dataset.dhash] = dataset
        self.count += 1
        self.size += dataset.size

    def delete_item(self, key: str):
        dataset = self.index.pop(key, None)
        if dataset:
            self.count -= 1
            self.size -= dataset.size

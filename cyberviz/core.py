import logging
from cyberviz.dataset import Dataset, CollectionDataset
from cyberviz.type import CsvDataset, PcapDataset

from streamlit.runtime.uploaded_file_manager import UploadedFile


class Cyberviz:
    def __init__(self):
        self.collection = CollectionDataset.new_collection()


    def add_dataset(self, path: str) -> bool:
        dataset = Dataset.new_dataset(path)
        if dataset is not None:
            self.collection.add_item(dataset)
            return True
        
        return False


    def load_dataset(self, data: UploadedFile) -> bool:
        dataset = Dataset.upload_dataset(data)
        if dataset is not None:
            self.collection.add_item(dataset)
            return True
        
        return False


    def activate(self, hash: str):
        ext = self.collection.index.get(hash).extension
        if ext == "csv":
            self.collection.index[hash].content = CsvDataset(self.collection.index.get(hash))
        
        elif ext == "pcap":
            self.collection.index[hash].content = PcapDataset(self.collection.index.get(hash))
        
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        self.collection.index[hash].content.load()


    def activate_all(self):
        for file_hash, _ in self.collection.index.keys():
            self.activate(file_hash)


    def get_preview(self, hash: str):
        data = self.collection.index.get(hash)
        if data is not None:
            if data.content is not None:
                data.content.preview()
            else:
                logging.warning(f"Dataset : {hash} must be activated first")
        else:
            logging.warning(f"Couldn't get dataset : {hash}")

    def delete(self, hash: str):
        self.collection.delete_item(hash)

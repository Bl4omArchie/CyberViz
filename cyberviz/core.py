from cyberviz.dataset import CsvDataset, PcapDataset, CollectionDataset
from streamlit.runtime.uploaded_file_manager import UploadedFile

import logging


class Cyberviz:
    def __init__(self):
        self.collection = CollectionDataset.new_collection()
        self.base_cls = {
            "csv": CsvDataset,
            "pcap": PcapDataset
        }

    def add_dataset(self, path: str) -> bool:
        extension = path.split('.')[-1].lower()
        base = self.base_cls.get(extension)

        if base is None:
            logging.warning(f"Unsupported file extension: {extension}")
            return False

        dataset = base.new_dataset(path)
        if dataset:
            self.collection.add_item(dataset)
            return True

        return False


    def load_dataset(self, data: UploadedFile) -> bool:
        extension = data.name.split('.')[-1].lower()
        base = self.base_cls.get(extension)

        if base is None:
            logging.warning(f"Unsupported file extension: {extension}")
            return False

        dataset = base.upload_dataset(data)
        if dataset:
            self.collection.add_item(dataset)
            return True

        return False


    def activate(self, hash: str):
        ext = self.collection.index.get(hash).extension
        print(ext)
        if ext == "csv":
            self.collection.index[hash].content = CsvDataset(self.collection.index.get(hash))
        
        elif ext == "pcap":
            self.collection.index[hash].content = PcapDataset(self.collection.index.get(hash))
        
        else:
            raise ValueError(f"Unsupported file type: {ext}")


    def activate_all(self):
        for file_hash, _ in self.collection.index.keys():
            self.activate(file_hash)


    def get_preview(self, hash: str):
        dataset = self.collection.index.get(hash)
        if dataset:
            return dataset.preview()
        logging.warning(f"Dataset : {hash} must be loaded first")


    def get_metadata(self, hash: str):
        dataset = self.collection.index.get(hash)
        if dataset:
            return dataset.metadata()
        logging.warning(f"Dataset : {hash} must be loaded first")


    def delete(self, hash: str):
        self.collection.delete_item(hash)

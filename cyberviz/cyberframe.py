from cyberviz.format import *

import dask.dataframe as dd
from pathlib import Path
import hashlib
import random
import os



# Main interface
class Cyberviz:
    """
    Cyberviz is a class that takes datasets and performs operations like compression, statistics, and more.
    Currently, only CSV, PCAP and Parquet files are accepted.
    """
    def __init__(self, datasets: dict=None):        
        # Dictionary to store loaded datasets with their unique IDs.
        # Usage: {hash1: Dataset1, hash2: Dataset2, ...}
        self.datasets = datasets
        self.activated_dataset = None
    
        
    @classmethod
    def upload_folder(cls, path: str) -> list[Dataset]:
        folder_path = Path(path)
        if not folder_path.is_dir():
            raise ValueError(f"[!] Path {path} is not a valid directory.")

        datasets = {}
        for file in folder_path.glob("*"):
            if file.suffix in [".csv", ".pcap", ".parquet", ".pq", ".parq"]:
                try:
                    data = create_dataset(str(file))
                    datasets[data.dhash] = data
                except Exception as e:
                    print(f"[!] Skipping {file}: {e}")

            else:
                print(f"[!] Skipping {file}. Incorrect format : {e}")

        return cls(datasets)


    @classmethod
    def update_file(cls, path: str) -> Dataset:
        file_path = Path(path)
        if not file_path.is_file():
            raise ValueError(f"[!] Path {path} is not a valid file.")

        if file_path.suffix in [".csv", ".pcap", ".parquet", ".pq", ".parq"]:
            data = create_dataset(str(file_path))

        return cls(datasets={data.hash: data})


    def activate(self, dhash_list: list, **kwargs):
        for dhash in dhash_list:
            self.activate_single(dhash)


    def activate_single(self, dhash: str, **kwargs):
        data = self.datasets.get(dhash)

        if data == None:
            raise ValueError("Incorrect dataset hash")
        
        if data.extension == "csv": 
            self.activate_dataset[data.hash] = CsvFormat(data)
        
        elif data.extension == "pcap": 
            self.activate_dataset[data.hash] = PcapFormat(data)

        elif data.extension in ["pq", "parquet", "parq"]: 
            self.activate_dataset[data.hash] = ParquetFormat(data)

        else:
            raise ValueError("Not supported dataset type.")


    def deactivate(self, dhash_list: list):
        for dhash in dhash_list:
            self.deactivate_single(dhash)


    def deactivate_single(dhash: str):
        if self.datasets.get(dhash) == None:
            raise ValueError("Incorrect dataset hash")

        del self.activate_dataset[dhash]


    # Create a new dataset based from several ones. The idea is to have a generic interface that works whatever
    # the dataset type. But as I haven't implemented yet every converting function, you can merge only dataset from the same type. 
    #
    # Parameter :
    #   list_dsid : ids of dataset you want to merge
    #
    # Returns :
    #   id of new dataset
    #
    def merge_dataset(self, dsid_to_merge: str, list_dsid: list):
        for dsid in list_dsid:
            if dsid not in self.ids:
                raise ValueError(f"[!] Invalid dsid : {dsid}")
            
            if dsid_to_merge == dsid:   # you can't merge a dataset to itself, it will skip to the next dataset
                print ("[!] Can't merge the same dataset to itself")
                continue
            
            self.datasets[dsid_to_merge].merge_headers(self.datasets[dsid])
            

    # Export a dataset to parquet format
    #
    #  Parameter :   
    #   dsid: dataset id
    #   export_path: folder where your file will be converted
    #
    def export_to_parquet(self, dsid: str, export_path: str):
        data = self.datasets.get(dsid)
        if data is None:
            raise ValueError("[!] Dataset not found")
        
        try:
            export_to_parquet(export_path)
            self.add_dataset(export_path)
            
        except Exception as e:
            print(f"[!] Failed to export dataset to parquet: {e}")


    # Get the hash of the dataset
    # Parameter :   
    #   dsid: dataset id
    # 
    # Return :
    #   hash of the dataset
    def get_hash(self, dsid: str) -> str:
        data = self.datasets.get(dsid)
        if data is None:
            raise ValueError("[!] Dataset not found")
        
        return data.hash_dataset

    
    # Take every loaded dataset and store them into a create_datalake
    # A datalake is defined as a single folder where only parquet file are stored
    # A json file keep track of each file to get them back to their original format
    # The purpose of the datalake is to store efficiently data for other purpose like data visualization or AI 
    #
    def create_datalake(self, folder="datalake/"):
        os.makedirs(folder, exist_ok=True)
        for dsid, dataset in self.datasets.items():
            path = os.path.join(folder, f"{dsid}.parquet")
            try:
                dataset.export_to_parquet(path)
            except Exception as e:
                print(f"[!] Failed to export {dsid}: {e}")


    def get_dataset(self, dsid: str):
        return self.datasets.get(dsid)

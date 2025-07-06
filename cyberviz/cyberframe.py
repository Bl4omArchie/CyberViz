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
    def __init__(self, datasets: dict):        
        # Dictionary to store loaded datasets with their unique IDs.
        # Usage: {id1: data_object1, id2: data_object2, ...}
        self.datasets = datasets
        self.ids = set()
    
        
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

        return cls(datasets)


    def update_file(self, path: str) -> Dataset:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[!] File {path} does not exist.")

        updated_dataset = create_dataset(path)

        return updated_dataset


    def add_dataset(self, path: str) -> str:
        file_path = Path(path)
        if not file_path.is_file():
            raise ValueError(f"[!] Path {path} is not a valid file.")

        if file_path.suffix(".csv"): 
            csv = CsvFormat()
            csv.update_file(path)
        
        elif file_path.suffix(".pcap"): 
            pcap = PcapFormat()
            pcap.update_file(path)
            
        elif file_path.suffix(".parquet", ".pq", ".parq"): 
            parquet = ParquetFormat()
            parquet.update_file(path)
            
        else:
            raise ValueError("[!] Invalid dataset format. Accepted formats: CSV, PCAP, Parquet") 

        if obj.dsid in self.ids:
            raise ValueError("[!] This dataset has already been loaded")
        
        self.ids.add(obj.dsid)
        self.datasets[obj.dsid] = obj
        
        return obj.dsid


    # Remove a dataset
    #
    # Parameters :
    #   dsid : dataset id
    #
    def remove_dataset(self, dsid: str):
        if dsid not in self.ids:
            raise ValueError("Dataset not found")

        self.ids.remove(dsid)
        del self.datasets[dsid]


    # Load one or several datasets. 
    #
    # Parameter :
    #   list_dsid : ids of dataset you want to merge
    #
    # Return :
    #   boolean value depending on the success of the activation
    #
    def activate_dataset(self, list_dsid: list, **kwargs) -> bool:
        # TODO : handle memory overflow
        for dsid in list_dsid:
            if dsid not in self.ids:
                raise ValueError("Dataset not found")

            self.datasets[dsid].activate_dataset(**kwargs)


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


    # Make basic analysis of the dataset
    #
    # Parameter :
    #   dsid: dataset id
    # 
    def analyze(self, dsid: str):
        if self.datasets.get(dsid).status == False:
            raise ValueError("[!] Inactive dataset, please active it first")
        self.datasets.get(dsid).basics_data()


    def get_dataset(self, dsid: str):
        return self.datasets.get(dsid)

from cyberviz.dataset import *
from cyberviz.export import *

import dask.dataframe as dd
import random
import os


class Cyberviz:
    """
    Cyberviz is a class that takes datasets and performs operations like compression, statistics, and more.
    Currently, only CSV, PCAP, and Parquet files are accepted.
    """
    
    def __init__(self):        
        # Dictionary to store loaded datasets with their unique IDs.
        # Usage: {id1: data_object1, id2: data_object2, ...}
        self.loaded_datasets = {}
        
        #Set of unique ids
        self.liste_id = set()
        
        
    # Generate an unique Datset ID (dsid)
    def generate_id(self):
        unique_id = 0x1
        while unique_id in self.liste_id:
            unique_id = random.randint(0, 0x1337)
        return unique_id
      
        
    # Add a dataset to the loaded_datasets dictionary
    # Parameter :
    #   path: path to the dataset emplacement
    #
    # Return :
    #   dsid: the unique id of the dataset
    def add_dataset(self, path: str):
        dsid = self.generate_id()
        if path.endswith(".csv"): 
            obj = CsvDataset(dsid, path)
        
        elif path.endswith(".pcap"): 
            obj = PcapDataset(dsid, path)
            
        elif path.endswith((".parquet", ".pq", ".parq")): 
            obj = ParquetDataset(dsid, path)
            
        else:
            raise ValueError("[!] Invalid dataset format. Accepted formats: CSV, PCAP, Parquet") 
        
        self.liste_id.add(dsid)
        self.loaded_datasets[obj.dsid] = obj
        
        return dsid
        

    # Make basic analysis of the dataset
    # Parameter :
    #   dsid: dataset id
    # 
    def analyze(self, dsid: int):
        self.loaded_datasets.get(dsid).open(chunksize=10, sep=",")


    # Export a dataset to parquet format
    # Parameter :   
    #   dsid: dataset id
    #   export_path: folder where your file will be converted
    def export_to_parquet(self, dsid: int, export_path: str):
        data = self.loaded_datasets.get(dsid)
        if data is None:
            raise ValueError("[!] Dataset not found")
        
        try:
            export_to_parquet(export_path)
            self.add_dataset(export_path)
            
        except Exception as e:
            print(f"[!] Failed to export dataset to parquet: {e}")
        
    
    # Take every loaded dataset and store them into a create_datalake
    # A datalake is defined as a single folder where only parquet file are stored
    # A json file keep track of each file to get them back to their original format
    # The purpose of the datalake is to store efficiently data for other purpose like data visualization or AI 
    def create_datalake(self):
        for val, key in self.loaded_datasets:
            print (val, key)
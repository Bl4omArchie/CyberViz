from cyberviz.convert.export import export_to_parquet
from cyberviz.formats.csv_ds import CsvDataset
from cyberviz.formats.pcap_ds import PcapDataset
from cyberviz.formats.hdf5_ds import Hdf5Dataset
from cyberviz.formats.parquet_ds import ParquetDataset
from cyberviz.formats.pickle_ds import PickleDataset
from cyberviz.dataset import *

import dask.dataframe as dd
import random
import os


class Cyberviz:
    """
    Cyberviz is a class that takes datasets and performs operations like compression, statistics, and more.
    Currently, only CSV, PCAP, HD5 and Parquet files are accepted.
    """
    
    def __init__(self):        
        # Dictionary to store loaded datasets with their unique IDs.
        # Usage: {id1: data_object1, id2: data_object2, ...}
        self.datasets = {}
        
        # Set of unique ids
        self.ids = set()
      
        
    # Add a dataset to the datasets dictionary
    # Parameter :
    #   path: path to the dataset emplacement
    #
    # Return :
    #   dsid: the unique id of the dataset
    def add_dataset(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"[!] The path {path} does not exist")

        if path.endswith(".csv"): 
            obj = CsvDataset(path)
        
        elif path.endswith(".pcap"): 
            obj = PcapDataset(path)
            
        elif path.endswith((".parquet", ".pq", ".parq")): 
            obj = ParquetDataset(path)
        
        elif path.endswith(".h5"):
            obj = Hdf5Dataset(path)
            
        elif path.endswith(".pickle"):
            obj = PickleDataset(path)
            
        else:
            raise ValueError("[!] Invalid dataset format. Accepted formats: CSV, PCAP, Parquet, HDF5") 

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
        
        self.all_ids.remove(dsid)
        del self.datasets[dsids]


    # Load one or several datasets into RAM. 
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
    def merge(self, dsid_to_merge: str, list_dsid: list):
        for dsid in list_dsid:
            if dsid not in self.ids:
                raise ValueError(f"[!] Invalid dsid : {dsid}")
            
            if dsid_to_merge == dsid:   # you can't merge a dataset to itself, it will skip to the next dataset
                print ("[!] Can't merge the same dataset to itself")
                continue
            
            self.datasets[dsid_to_merge].merge_dataset(self.datasets[dsid])
            

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
    def create_datalake(self):
        for key, val in self.datasets.items():
            print(key, val)


    # Make basic analysis of the dataset
    # Parameter :
    #   dsid: dataset id
    # 
    def analyze(self, dsid: str):
        self.datasets.get(dsid).open(chunksize=10, sep=",")
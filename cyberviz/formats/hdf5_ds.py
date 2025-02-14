from cyberviz.dataset import Dataset

import dask.dataframe as dd
import pandas as pd


class Hdf5Dataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".h5":
            raise ValueError("[!] HDF5 file only")
        else:
            self.format_dataset = "hdf5"
            self.extension_dataset = ".h5"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")
    
    
    # Load the hdf5 dataset into memory
    #
    def open_dataset(self):
        self.data = dd.read_hdf(self.path_dataset, 'r')
from cyberviz.dataset import Dataset

import dask.dataframe as dd
import pandas as pd



class PcapDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)
        
        if self.path_dataset.suffix != ".pcap":
            raise ValueError("[!] PCAP file only")
        else:
            self.format_dataset = "pcap"
            self.extension_dataset = ".pcap"

        if not self.path_dataset.is_file():
            raise ValueError("[!] Invalid path")
        
    def activate_dataset(self):
        self.status = True
        self.open_dataset()        

    def open_dataset(self):
        self.status = True
        self.data = open(self.path_dataset, 'rb')
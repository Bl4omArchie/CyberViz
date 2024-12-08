import os, re
import pandas as pd
import pyarrow.feather as feather

class Dataset:
    def __init__(self, file_name, file_path, file_type, sheet_name=None):
        self.filename = file_name
        self.filepath = file_path
        self.filetype = file_type
        if sheet_name != None:
            self.sheetname = sheet_name
       
        self.content = self.read_content()
        self.lexique = {
            "average": ["mean", "avg", "median", "average"],
            "total": ["sum", "tot", "total"],
            "minimum": ["min", "minimum"],
            "maximum": ["max", "maximum"],
            "standard_deviation": ["std", "stdev", "standard deviation"],
            "packet": ["pkt", "packets"],
            "bytes_per_second": ["b/s", "bytes/sec", "bytes per second"],
            "packets_per_second": ["p/s", "packets/sec", "packets per second"],
            "flow": ["traffic", "stream", "connection"],
            "forward": ["fwd", "forward"],
            "backward": ["bwd", "backward"],
            "flag": ["flg", "flag"],
            "window_size": ["win_size", "window size"],
            "segment": ["seg", "segment"],
            "rate": ["ratio", "rate"],
            "idle": ["inactivity", "idle"],
            "active": ["activity", "active", "act"],
            "header": ["hdr", "header"],
            "length": ["len", "length"],
            "duration": ["time", "duration"],
            "category": ["class", "type", "label"],
            "label": ["category", "label"]
        }
        
    def read_content(self):
        if self.filetype == "csv":
            if os.path.exists(f"feather/{self.filename}.feather"):
                return pd.read_feather(f"feather/{self.filename}.feather")
            else:
                df = pd.read_csv(self.filepath, low_memory=False)
                df.to_feather(f"feather/{self.filename}.feather")
                return df
        
        elif self.filetype == "xlsx":
            return pd.read_excel(self.filepath, sheet_name=self.sheetname)
        else:
            print ("[!] Unsupported filetype")
        
    def get_headers(self) -> list:
        return self.content.columns
    
    def get_reverse_lexique(self) -> list:
        return {synonym: key for key, synonyms in self.lexique.items() for synonym in synonyms}
    
    # Remove special caracters and lowercase headers
    def tokenize_headers(self) -> list:
        list_h = []
        for header in self.content.columns:
            list_h.append(re.findall(r'[a-zA-Z0-9]+|[^a-zA-Z0-9\s]', header.lower()))
        return list_h
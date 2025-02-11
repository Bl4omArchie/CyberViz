import os
import re


lexique = {
    "average": ["mean", "avg", "median"],
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
    "category": ["class", "type", "traffic_category"]
}

def get_reverse_lexique(self) -> list:
    return {synonym: key for key, synonyms in lexique.items() for synonym in synonyms}

# Remove special caracters and lowercase headers
def tokenize_headers(self, columns: list) -> list:
    tokenized_headers = []
    for header in columns:
        tokenized_headers.append(re.findall(r'[a-zA-Z0-9]+|[^a-zA-Z0-9\s]', header.lower()))
    
    return tokenized_headers
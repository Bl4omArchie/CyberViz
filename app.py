from src.cyber import *
from src.files import *


if __name__ == "__main__":
    dataset1 = Dataset("hiraki2021", "datasets/hiraki2021.csv", "csv")
    dataset2 = Dataset("cic-ids", "datasets/cic-ids.csv", "csv")

    #framework = CyberDataset([dataset1, dataset2])
    print (dataset1.get_headers())
    print (dataset2.get_headers())
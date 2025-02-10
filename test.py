from cyberviz.cyberviz import Cyberviz
from cyberviz.dataset import CsvDataset






if __name__ == "__main__":
    cz = Cyberviz()
    dsid1 = cz.add_dataset("data/hiraki2021.csv")

    cz.analyze(dsid1)
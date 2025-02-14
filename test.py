from cyberviz.main import Cyberviz



if __name__ == "__main__":
    cz = Cyberviz()
    dsid1 = cz.add_dataset("data/hiraki2021.csv")
    dsid2 = cz.add_dataset("data/cic-bot-iot.csv")

    cz.datasets.get(dsid1).activate_dataset(sep=",")
    cz.datasets.get(dsid2).activate_dataset(sep=",")

    cz.merge("cyberviz/interpreter/lexicon.json", [dsid1, dsid2])
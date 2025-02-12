from cyberviz.main import Cyberviz



if __name__ == "__main__":
    cz = Cyberviz()
    dsid1 = cz.add_dataset("data/hiraki2021.csv")
    dsid2 = cz.add_dataset("data/cic-bot-iot.csv")

    dsid1.activate(sep=",")
    dsid2.activate(sep=",")

    dsid1.merge_csv("cyberviz/interpreter/lexicon.json", dsid2)
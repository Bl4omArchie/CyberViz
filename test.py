from cyberviz.main import Cyberviz



if __name__ == "__main__":
    cz = Cyberviz()
    dsid1 = cz.add_dataset("data/hiraki2021.csv")
    dsid2 = cz.add_dataset("data/cic-bot-iot.csv")

    print (type(cz.get_hash(dsid1)))
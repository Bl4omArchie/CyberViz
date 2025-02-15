from cyberviz.main import Cyberviz



if __name__ == "__main__":
    cz = Cyberviz()
    
    dsid1 = cz.add_dataset("data/hiraki2021.csv")
    dsid2 = cz.add_dataset("data/NSL-KDD-V2.csv")
    dsid3 = cz.add_dataset("data/ISOT_Botnet_DataSet_2010.pcap")
    dsid4 = cz.add_dataset("data/scaler.pickle")

    cz.datasets.get(dsid1).activate_dataset(sep=",")
    cz.datasets.get(dsid2).activate_dataset(sep=",")
    cz.datasets.get(dsid3).activate_dataset()
    cz.datasets.get(dsid4).activate_dataset()

    cz.merge("cyberviz/interpreter/lexicon.json", [dsid1, dsid2])
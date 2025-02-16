from cyberviz.main import Cyberviz



if __name__ == "__main__":
    cz = Cyberviz()
    
    dsid1 = cz.add_dataset("data/hiraki2021.csv")
    dsid2 = cz.add_dataset("data/NSL-KDD-V2.csv")
    dsid3 = cz.add_dataset("data/ISOT_Botnet_DataSet_2010.pcap")
    #dsid4 = cz.add_dataset("data/scaler.pickle")

    cz.activate_dataset([dsid1, dsid2], sep=",")
    cz.activate_dataset([dsid3])
    """

    dsid1 = cz.add_dataset("data/cic-bot-iot.csv")
    dsid2 = cz.add_dataset("data/hiraki2021.csv")

    cz.activate_dataset([dsid1, dsid2], sep=",")
    """

    cz.merge(dsid1, [dsid2])
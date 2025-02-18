import cyberviz.mainframe as mf



if __name__ == "__main__":
    obj = mf.Cyberviz()
    
    """
    dsid1 = obj.add_dataset("data/hiraki2021.csv")
    dsid2 = obj.add_dataset("data/NSL-KDD-V2.csv")
    dsid3 = obj.add_dataset("data/ISOT_Botnet_DataSet_2010.pcap")
    #dsid4 = obj.add_dataset("data/scaler.pickle")

    obj.activate_dataset([dsid1, dsid2], sep=",")
    obj.activate_dataset([dsid3])
    """

    dsid2 = obj.add_dataset("data/cic-bot-iot.csv")
    dsid1 = obj.add_dataset("data/hiraki2021.csv")

    obj.activate_dataset([dsid1, dsid2], sep=",")

    obj.merge(dsid1, [dsid2])
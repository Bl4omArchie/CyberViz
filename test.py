import cyberviz.cyberframe as mf
from tests.test_tokenizer import *



def launch_test():
    unittest.main()

def load_dataset_test():
    obj = mf.Cyberviz()
    
    """
    dsid1 = obj.add_dataset("data/hiraki2021.csv")
    dsid2 = obj.add_dataset("data/NSL-KDD-V2.csv")
    dsid3 = obj.add_dataset("data/ISOT_Botnet_DataSet_2010.pcap")
    #dsid4 = obj.add_dataset("data/scaler.pickle")

    obj.activate_dataset([dsid1, dsid2], sep=",")
    obj.activate_dataset([dsid3])
    """

    dsid1 = obj.add_dataset("data/test_1.csv")
    dsid2 = obj.add_dataset("data/test_2.csv")

    obj.activate_dataset([dsid1, dsid2], sep=",")

    obj.merge_dataset(dsid1, [dsid2])


if __name__ == "__main__":
    #launch_test()
    load_dataset_test()
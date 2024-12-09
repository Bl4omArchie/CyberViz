from src.files import *
import spacy

class CyberViz:
    def __init__(self, dataset: list):
        # collection of dataset
        self.cdata = dataset
    
    def load_dataset(self, dataset: Dataset):
        self.cdata.append(dataset)
        
    def compare_headers(self):
        c_headers = []
        for data in self.cdata:
            c_headers.append(data.tokenize_headers())
        
        print (c_headers)
        #nlp = spacy.load("en_core_web_sm")
        #print (nlp(c_headers[0][10]))
        
"""
[['unnamed 01', 'unnamed 0', 'uid', 'originh', 'originp', 'responh', 'responp', 'flowduration', 'fwdpktstot', 'bwdpktstot', 'fwddatapktstot', 'bwddatapktstot', 'fwdpktspersec', 'bwdpktspersec', 'flowpktspersec', 'downupratio', 'fwdheadersizetot', 'fwdheadersizemin', 'fwdheadersizemax', 'bwdheadersizetot', 'bwdheadersizemin', 'bwdheadersizemax', 'flowfinflagcount', 'flowsynflagcount', 'flowrstflagcount', 'fwdpshflagcount', 'bwdpshflagcount', 'flowackflagcount', 'fwdurgflagcount', 'bwdurgflagcount', 'flowcwrflagcount', 'floweceflagcount', 'fwdpktspayloadmin', 'fwdpktspayloadmax', 'fwdpktspayloadtot', 'fwdpktspayloadavg', 'fwdpktspayloadstd', 'bwdpktspayloadmin', 'bwdpktspayloadmax', 'bwdpktspayloadtot', 
'bwdpktspayloadavg', 'bwdpktspayloadstd', 'flowpktspayloadmin', 'flowpktspayloadmax', 'flowpktspayloadtot', 'flowpktspayloadavg', 'flowpktspayloadstd', 'fwdiatmin', 'fwdiatmax', 'fwdiattot', 'fwdiatavg', 'fwdiatstd', 'bwdiatmin', 'bwdiatmax', 'bwdiattot', 'bwdiatavg', 'bwdiatstd', 'flowiatmin', 'flowiatmax', 'flowiattot', 'flowiatavg', 'flowiatstd', 'payloadbytespersecond', 'fwdsubflowpkts', 'bwdsubflowpkts', 'fwdsubflowbytes', 'bwdsubflowbytes', 'fwdbulkbytes', 'bwdbulkbytes', 'fwdbulkpackets', 'bwdbulkpackets', 'fwdbulkrate', 'bwdbulkrate', 'activemin', 'activemax', 'activetot', 'activeavg', 'activestd', 'idlemin', 'idlemax', 'idletot', 'idleavg', 'idlestd', 'fwdinitwindowsize', 'bwdinitwindowsize', 
'fwdlastwindowsize', 'trafficcategory', 'label'], 

['destinationport', 'flowduration', 'totalfwdpackets', 'totalbackwardpackets', 'totallengthoffwdpackets', 'totallengthofbwdpackets', 'fwdpacketlengthmax', 'fwdpacketlengthmin', 'fwdpacketlengthmean', 'fwdpacketlengthstd', 'bwdpacketlengthmax', 'bwdpacketlengthmin', 'bwdpacketlengthmean', 'bwdpacketlengthstd', 'flowbytess', 'flowpacketss', 'flowiatmean', 'flowiatstd', 'flowiatmax', 'flowiatmin', 'fwdiattotal', 'fwdiatmean', 'fwdiatstd', 'fwdiatmax', 'fwdiatmin', 'bwdiattotal', 'bwdiatmean', 'bwdiatstd', 'bwdiatmax', 'bwdiatmin', 'fwdpshflags', 'bwdpshflags', 'fwdurgflags', 'bwdurgflags', 'fwdheaderlength', 'bwdheaderlength', 'fwdpacketss', 'bwdpacketss', 'minpacketlength', 'maxpacketlength', 'packetlengthmean', 'packetlengthstd', 'packetlengthvariance', 'finflagcount', 'synflagcount', 'rstflagcount', 'pshflagcount', 'ackflagcount', 'urgflagcount', 'cweflagcount', 'eceflagcount', 'downupratio', 'averagepacketsize', 'avgfwdsegmentsize', 'avgbwdsegmentsize', 'fwdheaderlength1', 'fwdavgbytesbulk', 'fwdavgpacketsbulk', 'fwdavgbulkrate', 'bwdavgbytesbulk', 'bwdavgpacketsbulk', 'bwdavgbulkrate', 'subflowfwdpackets', 'subflowfwdbytes', 'subflowbwdpackets', 'subflowbwdbytes', 'initwinbytesforward', 'initwinbytesbackward', 'actdatapktfwd', 'minsegsizeforward', 'activemean', 'activestd', 'activemax', 'activemin', 'idlemean', 'idlestd', 'idlemax', 'idlemin', 'label']]

"""
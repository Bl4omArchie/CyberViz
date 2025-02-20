# Cyberviz

CyberViz is a tool for data visualization and manipulation of large dataset written in python.
The main purpose of the tool is to help people understanding one or several dataset correctly and perfom plenty of operation like AI training, dynamic visualization with graphs and more.

As the name suggest, this tool is oriented for cybersecurity so I'm principally developping features for security dataset like csv, pcap or logs. Of course, the tool isn't specific to this field and can adapted to other area like physic, maths or whatever field you want.

Features :
- Cyberviz handle the following format : csv, pcap, hdf5, parquet and more to come.
- Merge several dataset : intelligent manipulation to correlate several dataset into a single one
- Convert dataset : csv to pcap, csv to parquet ...
- Creation of datalake : a datalake is a byte stream of all of your dataset.
- AI training : pytorch integration for ML, DL...
- Plotting : display yout dataset through graphics

# Notes

In my commentaries, I use special tags for the purpose of each function.
- Feature : main function you can call to enjoy Cyberviz
- Requirement : function you have to call before using features
- Algorithm : functon useful for my features that you don't have to use

# Use cases

1- Open dataset
2- Dataset selection and first features (merge dataset)
3- Datalake : AI, Dataviz, Send dataset


Datasets (update 2025) :
- IoT-23 : https://www.stratosphereips.org/blog/2020/1/22/aposemat-iot-23-a-labeled-dataset-with-malicious-and-benign-iot-network-traffic
- Hiraki 2021 : https://zenodo.org/records/5199540
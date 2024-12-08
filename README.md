# Cybersecurity data visualization

In a traffic network, how can you distinct malicious packages from user legitimate packages ? 
I first tried to answered this question for a university project. I used the Hiraki2021 dataset and made a few graphics to understand malicious traffic.
This was very pleasant and now I want to develop the idea further with a full python project that take several datasets, make more accurate analysis with more graphics. 

I started wondering about malicious traffic from the day I installed Snort. At the moment, I asked myself : how can i write relevant rules to detect malicious traffic ?
I don't know anything about it and how behave a malicious traffic. My goal, with this project, is to learn about all type of attack, pcap files, malicious patterns and network security.


# Algorithms

The first issue you have when you process such dataset is semantic. When you want to make graph with one dataset it is easy because you take headers and make your plots. But when you have two datasets, it often happens that two different looking headers means the same thing. For example : **bwd_iat.avg** and **Bwd_IAT_Mean**. More that simple syntax issue such as uppercase or underscore, mean and average are synonim and avg is the abbreviation of average. How can I efficiently detect that those headers are actually the same ?

The process I imagined is the following:
1- clean the header : 
    bwd_iat.avg become  ["bwd", "iat", "avg"]
    Bwd_IAT_Mean become ["bwd", "iat", "mean"]

2- apply filters :
    2.1 Synonim filter :
    Use a reverse mapping dictionnary : {"mean": "average", "avg": "average","median": "average" ...} 
    So you fix the word you want in O(1) time.

    ["bwd", "iat", "avg"] become  ["bwd", "iat", "average"]
    ["bwd", "iat", "mean"] become ["bwd", "iat", "average"]

    2.2 Grammar filter :
    Words like flags and flag can cause confusion. Those details can be omitted for better recognition.

Now you can find out easily that those headers are the same !

But could it be more difficult ? Like in this case : flow_SYN_flag_count and SYN_Flag_Count. Lets try the algorithm.
1- clean the header :
    fwd_PSH_flag_count become ["flow", "syn", "flag", "count"]
    PSH_Flag_Count become ["syn", "flag", "count"]

2- No need of this part but...

My two string aren't equal. How can I easily understand there are similar ? Removing manually "flow" could be, in my opinion, too risky if, for example, there are several words to remove. This is could lead to confusion. Instead, I'm using the levenshtein ratio.

3- Levenshtein ratio

TODO


# Sources
## Dataset :
- [Hikari2021](https://zenodo.org/records/6463389)
- [ISOT](https://onlineacademiccommunity.uvic.ca/isot/datasets/)

## Python :
- [Pandas - data structure](https://pandas.pydata.org/pandas-docs/stable/index.html)
- [Feather - portable file format for storing Arrow tables or data frames](https://arrow.apache.org/docs/python/feather.html)

## Dataviz :
- [DatavizProject](https://datavizproject.com/)
- [Datawrapper](https://www.datawrapper.de/)

## Security :
- [Snort3 - NIDS](https://docs.snort.org/welcome)
- [Wireshark - Package sniffer](https://www.wireshark.org/)
from data_collection import load_tickers_from_pickle, load_tickers_to_pickle

import pandas as pd
import matplotlib.pyplot as pt

#data = load_tickers_from_pickle("../data/russel3000/0_data.pickle")
#data['ONB'].to_csv(r'./onb.csv')



#load_tickers_to_pickle(["^GSPC", "VIX"], "../data/snp500/0_data.pickle")
data = load_tickers_from_pickle("../data/snp500/0_data.pickle0")
print(type(data))
for k, v in data.items():
    data[k].to_csv("../data/snp500/" + str(k) + ".csv")
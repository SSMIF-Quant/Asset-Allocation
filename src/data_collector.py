import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
import seaborn as sns

class Data_Collector():

    def __init__(self):
        pass

    def get_ticker_stats(self, ticker, start, end):
        prices = yf.download(ticker, start=start, end=end)
        return prices

    def get_close_prices(self, ticker, start, end):
        prices = yf.download(ticker, start=start, end=end)
        return prices.Close

    def get_adj_close_prices(self, ticker, start, end):
        close_prices = yf.download(ticker, start=start, end=end)
        return close_prices["Adj Close"]

    def get_correlation_matrix(self, a, b, na="_eq_1", nb="_eq_2", plot=False):
        col_names_a = list(a.columns)
        col_names_b = list(b.columns)
        new_col_names_a = []
        new_col_names_b = []

        for index, _ in enumerate(col_names_a):
            new_col_names_a.append(col_names_a[index] + na)
            new_col_names_b.append(col_names_b[index] + nb)

        rename_dict_a = dict()
        rename_dict_b = dict()
        
        for index, _ in enumerate(col_names_a):
            rename_dict_a[col_names_a[index]] = new_col_names_a[index]
            rename_dict_b[col_names_b[index]] = new_col_names_b[index]

        a = a.rename(columns=rename_dict_a)
        b = b.rename(columns=rename_dict_b)

        df = pd.concat([a, b], axis=1, sort=False)

        corr_matrix = df.corr()
        if(plot == True):
            sns.heatmap(corr_matrix, annot=True)
            pt.show()
        
        return corr_matrix
    
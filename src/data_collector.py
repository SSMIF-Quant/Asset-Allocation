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

    def rename_columns(self, a, name):
        col_names = list(a.columns)
        new_col_names = []

        for index, _ in enumerate(col_names):
            new_col_names.append(col_names[index] + name)
        
        rename_dict = dict()

        for index, _ in enumerate(col_names):
            rename_dict[col_names[index]] = new_col_names[index]
        
        a = a.rename(columns=rename_dict)
        return a

    def get_correlation_matrix(self, a, b, na="_eq_1", nb="_eq_2", plot=False):

        a = self.rename_columns(a, name=na)
        b = self.rename_columns(b, name=nb)

        df = pd.concat([a, b], axis=1, sort=False)

        corr_matrix = df.corr()
        if(plot == True):
            sns.heatmap(corr_matrix, annot=True)
            pt.show()
        
        return corr_matrix

    def get_covariance_matrix(self, a, name="_eq_1", plot=False):
        cov_matrix = a.cov()
        if(plot == True):
            sns.heatmap(cov_matrix, annot=True)
            pt.show()
    
    def get_capm()
        return cov_matrix
    
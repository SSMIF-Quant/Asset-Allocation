
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
from data_collector import Data_Collector


if __name__ == "__main__":
    data_col = Data_Collector()
    start="2019-01-01"
    end="2020-01-01"


    msft_data = data_col.get_ticker_stats("MSFT", start=start, end=end)
    aapl_data = data_col.get_ticker_stats("AAPL", start=start, end=end)
    snp_data = data_col.get_ticker_stats("^GSPC", start=start, end=end)
    vix_data = data_col.get_ticker_stats("^VIX", start=start, end=end)
    #corr_aapl_msft = data_col.get_correlation_matrix(vix_data, snp_data)
    print(data_col.get_correlation_matrix(snp_data, vix_data, plot=True))


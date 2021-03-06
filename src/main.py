
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
from data_collector import Data_Collector
from benchmarker import Benchmarker

if __name__ == "__main__":
    data_col = Data_Collector()
    start="2019-02-01"
    end="2020-02-13"


    msft_data = data_col.get_ticker_stats("MSFT", start=start, end=end)
    aapl_data = data_col.get_ticker_stats("AAPL", start=start, end=end)
    #snp_data = data_col.get_ticker_stats("^GSPC", start=start, end=end)
    #vix_data = data_col.get_ticker_stats("^VIX", start=start, end=end)
    #corr_aapl_msft = data_col.get_correlation_matrix(vix_data, snp_data)
    #print(data_col.get_correlation_matrix(snp_data, vix_data, plot=True))
    #print(data_col.get_covariance_matrix(snp_data, vix_data, plot=True))
    #Ok, so first we will establish our benchmarks by pulling stocks from the DJIA
    #and claculating the historical return vector, the CAPM expected returns 
    #and the implied equilibrium return 
    #print(str(msft_data.index.values[0]).split("T")[0])
    #print(data_col.get_capm(msft_data, rf=".02"))
    #print(snp_data)
    #print(data_col.get_volatility(msft_data, "Adj Close"))
    #print(msft_data)
    print(data_col.get_volatility(msft_data, basis="Close"))
    print(data_col.get_capm(msft_data, .016))
   # print(data_col.get_covariance_matrix(msft_data, aapl_data, plot=False))
    #print(data_col.get_historical_returns(msft_data))
   # print(data_col.get_capm(msft_data, .02))
    # djia_equtities = data_col.get_ticker_stats(["AXP", "AAPL", "BA", "CAT", "CVX", "KO", "CSCO", "DIS"], start=start, end=end)
    # bench = Benchmarker(djia_equtities)
    # hist_returns_csco = bench.get_historical_returns("CSCO", basis="Volume")
    # print(hist_returns_csco)
    #print(djia_equtities.values[:,43][0])
    #print(djia_equtities.values[:,3][-1] - djia_equtities.values[:,3][0])
    #print(14892600-23833500)
    #print(1952500 - 4783200)
    #print(djia_equtities.columns.levels[1][0])
    #print(djia_equtities.values[:,1][0])
    # print(djia_equtities)
    #print(djia_equtities)
    #benchmark = Benchmarker()
    #print(benchmark.getExpectedTotalReturns(djia_equities))


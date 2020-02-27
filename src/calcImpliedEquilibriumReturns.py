#We will need to calculate the covariance matrix of the returns,
#the market caps of each of the assets in consideration
#the risk aversion rate
import pandas as pd
import yfinance as yf
import numpy as np

def getDailyReturns(equity_df, basis="Adj Close"):
    returns = [0]
    for i in range(1, len(equity_df[basis])):
        returns.append((equity_df[basis][i] - equity_df[basis][i-1])/equity_df[basis][i-1])
    
    return returns

def getCovarianceMatrixOfReturns(equities, basis="Adj Close"):
    basis_columns = []
    for equity in equities:
        basis_columns.append(getDailyReturns(equity, basis=basis))

    returns_df = pd.DataFrame(basis_columns)
    
    return returns_df.cov()

def getTickerStats(tickers, start, end):
        equity_df = []
        for ticker in tickers:
            equity_df.append(yf.download(ticker, start=start, end=end))
        
        return equity_df

if __name__ == "__main__":
    end = "2020-02-15"
    start = "2020-01-01"
    equities = ["HEDJ", "VZ", "STZ", "GOOG", "AMGN", "EMR", "GILD", "FMC"]
    market_caps = [1.63, 227.72, 33.64, 904.62, 131.4, 39.39, 91.18, 11.97]
    equity_df = getTickerStats(equities, start=start, end=end)
    print(equity_df)
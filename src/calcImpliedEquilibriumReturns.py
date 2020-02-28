#We will need to calculate the covariance matrix of the returns,
#the market caps of each of the assets in consideration
#the risk aversion rate
import pandas as pd
import yfinance as yf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as pt

def getDailyReturns(equity_df, basis="Adj Close"):
    returns = [0]
    for i in range(1, len(equity_df[basis])):
        returns.append((equity_df[basis][i] - equity_df[basis][i-1])/equity_df[basis][i-1])
    
    return returns

def getCovarianceMatrixOfReturns(equities, basis="Adj Close"):
    basis_columns = []
    for equity in equities:
        basis_columns.append(getDailyReturns(equity, basis=basis))
########################################TESTING CONTENT############################################

    basis_columns = [[],[],[],[]]


########################################TESTING CONTENT#############################################
    basis_columns = basis_columns.T
    X = pd.DataFrame(basis_columns)
    
    #time for the math
    #first we will transform the raw data matrix X into deviation scores for matrix x
    #x = X - 11'X (1.0/n) where 
    # X is an n x k matrix of returns, x is an n x k matrix of deviation scores, and 1 is an n x 1 column 
    # vector of ones
    n = len(basis_columns[0])
    one = np.ones(n)

    #x = X - (1.0/n) * 11'X
    x = np.subtract(X, (1/n) * (np.multiply(np.multiply(one, one.transpose()),X))  )

    #Then we will compute x'x, the k x k deviation sums of squares and cross products matrix for x
    dev_ss_cp = np.multiply(x.transpose(), x)

    #then we will divide each term in the deviation sum of squares and cross products by n to create the variance 
    #covariance matrix
    V  = dev_ss_cp * (1/n)

    #V should be a k x k (num assets x num assets) variance covariance matrix (aka covariance matrix) for the 
    #columns input into the function

    return V

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
    #equity_df = getTickerStats(equities, start=start, end=end)
    #print(equity_df)
    #print(getCovarianceMatrixOfReturns(equity_df, basis="Adj Close"))
    
#We will need to calculate the covariance matrix of the returns,
#the market caps of each of the assets in consideration
#the risk aversion rate
import pandas as pd
import yfinance as yf
import numpy as np
import seaborn as sns
import pandas_datareader as pdr
import matplotlib.pyplot as pt

def getDailyReturns(equity_df, basis="Adj Close"):
    returns = []
    basis_columns = []
    #ok, so we have a list of dataframes and we need to get certain columns from each
    for frames in equity_df:
        basis_columns.append(frames[basis])
    
    for col in basis_columns:
        returns.append(col.pct_change().fillna(0))
    
    return returns

# def getCovarianceMatrixOfReturns():
#def getCovarianceMatrixOfReturns(lists):
def getCovarianceMatrixOfReturns(equities, start, end, basis="Adj Close"):
#This implementation is based off of this example https://stattrek.com/matrix-algebra/covariance-matrix.aspx

    # basis_columns = []
    
    # for index, equity in enumerate(equities):
    #     print(equity)
    #     basis_columns.append(list(getTickerStats(equity, start=start, end=end)[0][basis].values))

    # for index, col in enumerate(basis_columns):
    #     basis_columns[index] = getPercentChange(col)

    equity_df = getTickerStats(equities, start=start, end=end)

    basis_columns = getDailyReturns(equity_df)
    # for scores in lists:
    #     basis_columns.append(scores)
########################################TESTING CONTENT############################################
#each sub list represents a different "student's test scores" in math english and art

    # basis_columns = [[90, 60, 90],
    #                  [90, 90, 30],
    #                  [60, 60, 60],
    #                  [60, 60, 90],
    #                  [30,30,30]]

    # basis_columns = [[90,90,60,60,30], [60,90,60,60,30], [90,30,60,90,30]]

########################################TESTING CONTENT#############################################

    X = np.array(basis_columns).T.tolist()

    print("\n#############################\n")
    print("Raw Data:")
    print(X)
    
    #time for the math
    #first we will transform the raw data matrix X into deviation scores for matrix x
    #x = X - 11'X (1.0/n) where 
    # X is an n x k matrix of returns, x is an n x k matrix of deviation scores, and 1 is an n x 1 column 
    # vector of ones

    n = len(X)
    print(n)
    #one = 11'
    one = np.ones((n,n))

    #x = X - (1.0/n) * 11'X
    x = np.subtract(X, np.multiply( (1/n), np.matmul(one, X) ))

    #Then we will compute x'x, the k x k deviation sums of squares and cross products matrix for x
    dev_ss_cp = np.matmul(x.transpose(), x)
    
    #then we will divide each term in the deviation sum of squares and cross products by n to create the variance 
    #covariance matrix
    V  = np.multiply((1/n), dev_ss_cp)

    print("\n#############################\n")
    print("Variance-Covariance Matrix:")
    print(V)
    print("\n#############################\n")

    #V should be a k x k (num assets x num assets) variance covariance matrix (aka covariance matrix) for the 
    #columns input into the function
    #The diagonal of V is the variance of returns for each equity and the covariance is represented by the 
    #off diagonal elements of V
    # sns.heatmap(V)
    # pt.show()
    return V

def getCovarianceMatrixOfReturns2(equities, start, end, basis="Adj Close"):
    basis_df = pdr.DataReader(["STZ"], 'yahoo', start=start, end=end)[basis]
    #V = np.multiply(basis_df.pct_change().dropna().cov(), (len(basis_df) - 1) / len(basis_df))
    #print(V)
    basis_col = basis_df["STZ"]
    change = basis_col.pct_change()
    variance = (change.std() * (len(change)-1)/(len(change)))**2
    print(variance)    
    #return V

def getTickerStats(tickers, start, end):
        equity_df = []
        for ticker in tickers:
            equity_df.append(yf.download(ticker, start=start, end=end))
        
        return equity_df

if __name__ == "__main__":
    end = "2020-02-01"
    start = "2020-01-01"
    # equities = ["HEDJ", "VZ", "STZ", "GOOG", "AMGN", "EMR", "GILD", "FMC"]
    equities = ["HEDJ", "VZ", "STZ", "GOOG", "EMR"]
    market_caps = [1.63, 227.72, 33.64, 904.62, 131.4, 39.39, 91.18, 11.97]
    #equity_df = getTickerStats(equities, start=start, end=end)
    #print(equity_df)
    #print(getCovarianceMatrixOfReturns(equity_df, basis="Adj Close"))
    # getCovarianceMatrixOfReturns([[90, 60, 90], [90,90,30], [60,60,60], [60,60,90], [30,30,30]])
    getCovarianceMatrixOfReturns(equities, start=start, end=end, basis="Adj Close" )
    getCovarianceMatrixOfReturns2(equities, start=start, end=end, basis="Adj Close" )
    #print(getDailyReturns(getTickerStats(["HEDJ"], start=start, end=end)))
    #thing = getTickerStats(["HEDJ"], start=start, end=end)
    #print(getDailyReturns(thing))
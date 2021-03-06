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
        
        return cov_matrix

    def get_target_column(self, equity, basis):
        return equity[basis].values

    def get_residuals(self, target):
        residuals = [0]
        for i in range(1, len(target)):
            residuals.append(target[i] - target[i-1])
        
        return residuals

    def get_percent_change(self, target):
        residuals = [0]
        for i in range(1, len(target)):
            residuals.append(((target[i] - target[i-1])/target[i-1]) * 100)
        
        return residuals

    def get_volatility(self, ticker, basis):
        target_column = self.get_target_column(ticker, basis)
        #residuals = self.get_residuals(target_column)
        #volatility = np.std(residuals)
        # mean = np.mean(target_column)
        # residuals = []
        # sum = 0
        # for price in target_column:
        #     residuals.append((price - mean)**2)
        # for price in residuals:
        #     sum += price
        # volatility = np.sqrt(sum / len(target_column))

        return np.std(target_column)

    def get_historical_returns(self, equity, basis="Adj Close"):
        return ((equity[basis][-1] - equity[basis][0]) / equity[basis][0]) * 100

    def get_capm(self, equity, rf, basis="Adj Close"):
        #for the market returns we will use historical returns over the time period
        #of the data given
        start = str(equity.index.values[0]).split("T")[0]
        end = str(equity.index.values[-1]).split("T")[0]
        snp_data = self.get_ticker_stats("^GSPC", start=start, end=end)

        target_column = self.get_target_column(equity, basis)
        market_column = self.get_target_column(snp_data, basis)
        #these are historical returns
        #target_returns = (target_column[-1] - target_column[0]) / (target_column[0])
        market_return = ((snp_data[basis][-1] - snp_data[basis][0]) / (snp_data[basis][0])) * 100
        #target_risk_premium = target_returns - rf
        market_risk_premium  = market_return - (rf * 100)

        #beta = cov(r_a, r_m) / var(r_m)
        target_residuals = self.get_percent_change(target_column)
        market_residuals = self.get_percent_change(market_column)
        df = pd.DataFrame({"Asset Returns" : target_residuals, "Market Returns" : market_residuals})
        
        x_bar = np.mean(target_residuals)
        y_bar = np.mean(market_residuals)
        sum = 0
        for i in range(len(target_column)):
            sum += ((target_residuals[i] - x_bar)*(market_residuals[i] - y_bar))
        cov = sum/len(target_column-1)

        var = np.std(market_residuals)**2

        beta = cov / var
        # corr = df.corr().values[1][0]
        # var_target = self.get_volatility(target_residuals)**2
        # var_market = self.get_volatility(market_residuals)**2
        # beta = corr * (var_target/var_market)

        capm = rf + beta * (market_risk_premium) 

        return capm, beta, market_risk_premium
    

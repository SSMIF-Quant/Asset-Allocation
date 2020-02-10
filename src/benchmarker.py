#this class will provide estimates of expected total return based off of historical, CAPM and implied equilibrium return
import numpy as np

class Benchmarker():

    def __init__(self, equities):
        self._equities = equities
        self._metrics = list(equities.columns.levels[0])
        self._ticker_names = list(equities.columns.levels[1])
    
    def get_target_column(self, equities, ticker, basis):
        metrics = list(equities.columns.levels[0])
        ticker_names = list(equities.columns.levels[1])
        if ticker in ticker_names:
            ticker_index = ticker_names.index(ticker)
        if basis in metrics:
            metric_index = metrics.index(basis)

        index = ((metric_index+1) * 8) - (len(ticker_names) - ticker_index)
        target_column = np.asarray(equities.values[:,index])
        
        return target_column

    def get_historical_returns(self, ticker, basis="Adj Close"):
        target_column = self.get_target_column(self._equities, ticker, basis)
        hist_returns = target_column[-1] - target_column[0]

        return hist_returns

    

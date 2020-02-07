#this class will provide estimates of expected total return besed off of historical, CAPM and implied equilibrium return

class Benchmarker():

    def __init__(self, equities):
        self._equities = equities
        self._metrics = list(equities.columns.levels[0])
        self._ticker_names = list(equities.columns.levels[1])
    
    def calculate_historical_returns(self, ticker, basis="Adj Close"):
        if ticker in self._ticker_names:
            ticker_index = self._ticker_names.index(ticker)
        if basis in self._metrics:
            metric_index = self._metrics.index(basis)
        
        index = ((metric_index+1) * 8) - (len(self._ticker_names) - ticker_index)
        hist_returns = self._equities.values[:,index][-1] - self._equities.values[:,index][0]

        return hist_returns
        #ticker = np.asarray(ticker)
        #return (ticker[-1] - ticker[0])
    

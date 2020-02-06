from categorical_transformer import CategoricalTransformer
from alpha_vantage.timeseries import TimeSeries
from sklearn.pipeline import Pipeline
import pandas as pd

# this will be the "main" file for a script which will determine allocation sizes in small 
# medium and large cap stocks in the s&p 500
# We will need some way to filter based off of a condition when we pass a list of stocks in
#We will construct a pipeline using sklearn.pipeline.Pipeline which will call a series of fit transforms
#on passed in objects and data and then call fit on the final estimator

if __name__ == "__main__":
    # tickers = ['AAPL', 'MSFT', '^GSPC']

    # start_date = '2010-01-01'
    # end_date = '2020-01-01'

    # ts = TimeSeries(key='ABAZG3640N63KZE4', output_format='pandas')
    # data, meta_data = ts.get_intraday(symbol='MSFT', interval="1min", outputsize='full')
    # print(data)
    # print("######################@@@@@@@@@@@@@@@@@@@###############")
    # print(meta_data)
    path = "../data/credit-data-trainingset.csv"
    data = pd.read_csv(path)
    cat_features = ["age", "revolving_utilization_of_unsecured_lines"]
    print(data[cat_features])
    pipeline = Pipeline(steps=[('cat_transformer', CategoricalTransformer(cat_features))])
    output = pipeline.transform(data)
    print(output)
    
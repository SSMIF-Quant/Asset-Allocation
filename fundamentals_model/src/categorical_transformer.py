import numpy as np
import pandas as pd
import matplotlib.pyplot as pt
from pandas_datareader import data
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, FeatureUnion

class CategoricalTransformer(BaseEstimator, TransformerMixin):
    #constructor
    def __init__(self, feature_names):
        self._feature_names = feature_names
        self._transformed_feature_names = []

    #return selfm we will do nothing here
    def fit(self):
        return self

    #The meat and potatoes of this class will be transform
    #the commented version of the function below will return only a data frame of the selected  columns from 
    #the original input, X
    def transform(self, X, y=None):
        # for i, column in enumerate(self._feature_names):
        #     for index, value in enumerate(column):
        #         if(index == 0):
        #             continue
        #         elif(column[index] < column[index-1]):
        #             X[str(self._feature_names[i]) + "_cat"] = -1
        #         elif(column[index] == column[index-1]):
        #             X[str(self._feature_names[i]) + "_cat"] = 0
        #         elif(column[index] > column[index-1]):
        #             X[str(self._feature_names[i]) + "_cat"] = 1

        # for i in self._feature_names:
        #     self._transformed_feature_names.append(i + "_cat")

        for index, _ in enumerate(self._feature_names):
            temp_str = self._feature_names[index] + "_cat"
            self._transformed_feature_names.append(temp_str)
        

        for i, features in enumerate(self._feature_names):
            for index, rows in enumerate(features):
                if index == 0:
                    X[self._transformed_feature_names[i]] = 0
                else:
                    X[self._transformed_feature_names[i]] = 1

        for name in self._transformed_feature_names:
            self._feature_names.append(name)

        return X[self._feature_names]


    #Here is where we will start to try to develop some financial ratios

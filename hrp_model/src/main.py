# The objective of this model is to take in a set of time-series inputs and return optimal portfolio weightings
# for each


# Three stages of HRP:
# Tree Clustering: group similar investments into clusters 
# based on their correlation matrix. Having a hierarchical 
# structure helps us to improve stability issues of quadratic 
# optimizers when inverting the covariance matrix.

# Quasi-diagonalization:
# reorganize the covariance matrix so similar investments will 
# be placed together. This matrix diagonalization allow us to 
# distribute weights optimally following an inverse-variance 
# allocation.

# Recursive Bisection:
# distribute the allocation through recursive bisection based on 
# cluster covariance.


import scipy.cluster.hierarchy as sch
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as pt
import cvxopt as opt
from cvxopt import blas, solvers
from alpha_vantage.timeseries import TimeSeries
import ffn
import config

if "__name__" == __main__:
    pass
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

import sys
#to compile this you need to have biclustlib installed onto your machine 
#the link to their github is: https://github.com/padilha/biclustlib
#get that, set up a virtualenv using the instructions in the create_ssmif_env.sh script 
# (it just prints what you should do)
#then, run the build_hrp.sh script which will install the dependencies needed for biclustlib
#then you should run python setup.py install in the root directory of the biclustlib package
#after that, you should be able to run this package
sys.path.insert(0, "/home/mycicle/ssmif/biclustlib")
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
from biclustlib.algorithms import BiCorrelationClusteringAlgorithm
#up first, correlation clustering functions
# We will use BCCA Bi-Correlation Clustering Algorithm
# for this implementation
# We get the package from this source
#  Padilha, V. A. & Campello, R. J. G. B. (2017).
#  A systematic comparative evaluation of biclustering techniques. BMC Bioinformatics, 18(1):55.

def correlationCluster(data):
    pass
if __name__ == "__main__":
    data = dict()

    #clusters = correlationCluster(data)
    #qdiag = quasiDiagonalization(clusters)
    #allocations = recBisection(qdiag)
    #print(allocations)
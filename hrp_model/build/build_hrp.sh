#!/bin/bash

pip install -U pip
sudo apt-get install libgmp-dev libmpfr-dev libmpc-dev
python3 -m pip install scipy numpy matplotlib pandas datetime cvxopt alpha_vantage cython scikit-learn bottleneck munkres fabia ffn config gmpy
sudo apt install python-rpy2 python-gmpy
sudo apt install python3-tk
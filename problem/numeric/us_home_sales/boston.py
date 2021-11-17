#! /usr/bin/env python
#
# Copyright 2021 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or
# other liability, whether in an action of contract, tort or otherwise,
# arising from, out of or in connection with the software or the use or
# other dealings in the software.
#
from sklearn.metrics import mean_squared_error
import pandas as pd
import xgboost as xgb


# cf https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html
def _load_boston():
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep=r'\s+', skiprows=22, header=None)
    # data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    # target = raw_df.values[1::2, 2]
    assert (1012, 11) == raw_df.shape
    return raw_df


# from https://www.datacamp.com/community/tutorials/xgboost-in-python
def predict_boston_home_prices():
    data = _load_boston()
    x, y = data.iloc[:,:-1],data.iloc[:,-1]
    data_dmatrix = xgb.DMatrix(data=X,label=y)



if __name__ == '__main__':
    predict_boston_home_prices()

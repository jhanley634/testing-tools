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
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.datasets
import sklearn.metrics
import sklearn.model_selection

from problem.util.web_file import WebFile


def _get_sales_subset(url='https://www.sector6.net/2021/11/us_home_sales.csv.xz'):
    df = pd.read_csv(WebFile(url).file())
    assert 30 == len(df.dtypes)
    assert '2017-01-03' == df.saledate.min()
    assert '2018-08-02' == df.saledate.max()
    assert 99_500_000 == df.saleprice.max()

    df = df[df.saledate < '2017-02-01']
    df = df[df.saleprice < 9_000_000].reset_index()

    cols = 'saledate saleprice areabuilding bathcount'.split()
    df = df[cols]

    return df


def price_regression():
    df = _get_sales_subset()
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        df[['areabuilding', 'bathcount']], df.saleprice, random_state=2)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    predicted = lr.predict(x_test)
    np.sum(np.abs(y_test - predicted)) / len(y_test)

    fig, ax = plt.subplots()
    ax.scatter(y_test, predicted)
    ax.set_xlabel('test (observed) price')
    ax.set_ylabel('predicted price')
    plt.show()


if __name__ == '__main__':
    price_regression()

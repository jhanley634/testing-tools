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
from io import StringIO
from pathlib import Path

from more_itertools import peekable
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import xgboost as xgb


def _decode_lines(resp):
    for line in resp.iter_lines():
        yield line.decode()


def _read_data_lines(boston_url='http://lib.stat.cmu.edu/datasets/boston'):
    """Impedance matches from stanzas to CSV lines.

    A .csv file is expected to have lines, that is, a newline after each row.
    The fetched document has been line wrapped with 1st line of each stanza having max width of 75,
    then 2nd line starts with SPACE and usually has 22 characters.
    We combine these two-line stanzas, turning each into a single CSV row.
    """
    with requests.get(boston_url, stream=True) as resp:
        resp.raise_for_status()
        lines = peekable(_decode_lines(resp))

        for line in lines:
            nxt = lines.peek('')
            if nxt.startswith(' '):
                nxt = next(lines)  # consume it
                yield f'{line}{nxt}'
            else:
                yield line


# cf https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html
def _load_boston() -> pd.DataFrame:
    cols = 'CRIM ZN INDUS CHAS NOX RM AGE DIS RAD TAX PTRATIO B LSTAT MEDV'
    lines = StringIO('\n'.join(_read_data_lines()))
    raw_df = pd.read_csv(lines, sep=r'\s+', skiprows=22, header=None, names=cols.split())
    # data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    # target = raw_df.values[1::2, 2]
    assert (496, 14) == raw_df.shape
    return raw_df.dropna()  # drops a single NaN row


# from https://www.datacamp.com/community/tutorials/xgboost-in-python
def predict_boston_home_prices():
    data = _load_boston()
    print(data.describe())
    data.to_csv(Path('~/Desktop').expanduser() / 't.csv')
    x, y = data.iloc[:, :-1], data.iloc[:, -1]
    data_dmatrix = xgb.DMatrix(data=x, label=y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)
    xg_reg = xgb.XGBRegressor(objective='reg:squarederror',
                              colsample_bytree=0.3,
                              learning_rate=0.1,
                              max_depth=5,
                              alpha=10,
                              n_estimators=10)
    xg_reg.fit(x_train, y_train)
    preds = xg_reg.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    assert 6.263944 == round(rmse, 6), rmse

    params = {'objective': 'reg:squarederror',
              'colsample_bytree': 0.3,
              'learning_rate': 0.1,
              'max_depth': 5,
              'alpha': 10}
    cv_results = xgb.cv(dtrain=data_dmatrix,
                        params=params,
                        nfold=3,
                        num_boost_round=50,
                        early_stopping_rounds=10,
                        metrics='rmse',
                        as_pandas=True,
                        seed=123)
    print(cv_results.head())
    print((cv_results['test-rmse-mean']).tail(1))

    xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=10)

    matplotlib.use('MacOSX')
    xgb.plot_tree(xg_reg,num_trees=0)
    plt.rcParams['figure.figsize'] = [50, 10]
    plt.show()


if __name__ == '__main__':
    predict_boston_home_prices()

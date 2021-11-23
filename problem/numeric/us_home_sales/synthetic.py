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
import random as rnd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb


def _attr_name(n: int) -> str:
    """Maps num -> name.

    >>> _attr_name(7)
    'attr007'
    """
    return f'attr{n:03d}'


def _response_function(attr0, attr1, thresh=0.1):
    if (attr0 < thresh
            or attr1 < thresh):
        return 0.0
    return attr0 + attr1


def gen_synthetic_dataset(num_attrs=3, num_informative_attrs=2,
                          num_rows=10_000, avg=0.0, sigma=1.0) -> pd.DataFrame:
    perm = list(range(num_attrs))
    rnd.shuffle(perm)  # Permutation of attr indices, where 0 & 1 are conjunction.
    print(perm)
    rows = []
    for _ in range(num_rows):
        d = {_attr_name(j): rnd.gauss(avg, sigma)
             for j in range(num_attrs)}
        inf_attrs = [d[_attr_name(perm[j])]
                     for j in range(num_informative_attrs)]
        d['y'] = _response_function(*inf_attrs)
        rows.append(d)

    return pd.DataFrame(rows)


def main():
    data = gen_synthetic_dataset()

    x, y = data.iloc[:, :-1], data.iloc[:, -1]
    data_dmatrix = xgb.DMatrix(data=x, label=y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)
    xg_reg = xgb.XGBRegressor(objective='reg:squarederror',
                              )
    xg_reg.fit(x_train, y_train)
    preds = xg_reg.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    assert rmse < .1, rmse

    params = {'objective': 'reg:squarederror',
              }
    cv_results = xgb.cv(dtrain=data_dmatrix,
                        params=params,
                        metrics='rmse',
                        as_pandas=True)
    print(cv_results.head())
    print((cv_results['test-rmse-mean']).tail(1))

    xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=10)

    matplotlib.use('MacOSX')
    xgb.plot_tree(xg_reg, num_trees=0)
    plt.rcParams['figure.figsize'] = [50, 10]

    xgb.plot_importance(xg_reg)
    plt.rcParams['figure.figsize'] = [5, 5]
    plt.show()

if __name__ == '__main__':
    main()

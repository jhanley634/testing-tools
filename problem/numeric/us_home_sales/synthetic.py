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
from itertools import combinations
import random as rnd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb


def _band_indicator(n: float, scale=0.2) -> float:
    """Zeros out alternate bands of the input.

    Here, zeroed bands are e.g. [0 .. .2), [.4 .. .6), etc.
    """
    s = int(n / scale)
    if s % 2 == 0:
        return 0
    return 1


def _get_two_informative_attr_names(xg_reg) -> (str, str):
    v_k = reversed(sorted((v, k)
                          for k, v in xg_reg.get_fscore().items()))
    names = [k
             for v, k in v_k]
    assert names[0].startswith('sum_attr')
    assert names[1].startswith('attr')
    assert names[2].startswith('attr')
    return names[1], names[2]


def _attr_name(n: int) -> str:
    """Maps num -> name.

    >>> _attr_name(7)
    'attr007'
    """
    return f'attr{n:03d}'


THRESH = 0.1


def _response_function(attr0, attr1):
    if (attr0 < THRESH
            or attr1 < THRESH):
        return 0.0
    return attr0 + attr1


def gen_synthetic_dataset(num_attrs=20, num_informative_attrs=2,
                          num_rows=20_000, avg=0.0, sigma=1.0, permute=True) -> pd.DataFrame:

    attr_indexes = list(range(num_attrs))
    perm = attr_indexes.copy()
    if permute:
        rnd.shuffle(perm)  # Permutation of attr indices, where 0 & 1 are conjunction.
        print(perm)
    rows = []
    for _ in range(num_rows):
        d = {_attr_name(j): rnd.gauss(avg, sigma)
             for j in range(num_attrs)}
        for a, b in combinations(attr_indexes, 2):
            d[f'sum_{_attr_name(a)}_{_attr_name(b)}'] = (
                    d[_attr_name(a)]
                    + d[_attr_name(b)]
            )
        for j in range(num_attrs):
            indicator_name = f'ind{j:03d}'
            d[indicator_name] = int(d[_attr_name(j)] > THRESH)  # an indicator is 0 or 1
        inf_attrs = [d[_attr_name(perm[j])]
                     for j in range(num_informative_attrs)]
        d['y'] = _response_function(*inf_attrs)
        rows.append(d)

    return pd.DataFrame(rows)


def main():
    data = gen_synthetic_dataset()
    x, y = data.iloc[:, :-1], data.iloc[:, -1]
    data_dmatrix = xgb.DMatrix(data=x, label=y)

    params = {
        'objective': 'reg:squarederror',
        'booster': 'gbtree',  # 'dart',
    }
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    xg_reg = xgb.XGBRegressor(**params)
    xg_reg.fit(x_train, y_train)
    preds = xg_reg.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print('RMSE:', rmse)
    assert rmse < .6, rmse

    cv_results = xgb.cv(dtrain=data_dmatrix, params=params)
    print(cv_results)

    xg_reg = xgb.train(dtrain=data_dmatrix, params=params)

    matplotlib.use('MacOSX')
    _, ax = plt.subplots(nrows=3)
    xgb.plot_tree(xg_reg, num_trees=0, ax=ax[0])

    xgb.plot_importance(xg_reg, ax=ax[1])

    inf0, inf1 = _get_two_informative_attr_names(xg_reg)
    plt.scatter(x_test[inf0], [_band_indicator(x1) * y
                               for x1, y in zip(x_test[inf1], y_test)])
    plt.show()


if __name__ == '__main__':
    main()

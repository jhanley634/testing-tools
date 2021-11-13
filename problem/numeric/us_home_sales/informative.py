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
from sklearn.model_selection import KFold, cross_val_score
from xgboost import XGBRegressor, plot_importance
import matplotlib
import matplotlib.pyplot as plt
import sklearn
import xgboost as xgb

from problem.numeric.us_home_sales.us_home_sales import _get_sales_subset


def find_informative_attrs():
    df = _get_sales_subset()
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        df.copy().drop(['saleprice'], axis=1), df.saleprice)
    model = XGBRegressor(max_depth=20, n_estimators=500)
    kfold = KFold(n_splits=5)
    results = cross_val_score(model, x_train, y_train, cv=kfold)
    print("Accuracy: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

    model.fit(x_train, y_train)
    matplotlib.use('MacOSX')
    fig, ax = plt.subplots(2)
    plot_importance(model, ax=ax[0], max_num_features=7)

    y_pred = model.predict(x_test)
    plt.scatter(y_test, y_pred)
    plt.show()


if __name__ == '__main__':
    find_informative_attrs()

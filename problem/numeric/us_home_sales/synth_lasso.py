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
from numpy import absolute, mean, std
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import RepeatedKFold, cross_val_score, train_test_split
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from problem.numeric.us_home_sales.synthetic import gen_synthetic_dataset


def _get_mtcars_x_y():
    url = 'https://raw.githubusercontent.com/Statology/Python-Guides/main/mtcars.csv'
    data_full = pd.read_csv(url)
    x = data_full[['mpg', 'wt', 'drat', 'qsec']]
    y = data_full['hp']
    return x, y


def main():

    data = gen_synthetic_dataset(num_rows=20_000, permute=False)

    x, y = data.iloc[:, :-1], data.iloc[:, -1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    #
    if False:
        x, y = _get_mtcars_x_y()
        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        model = LassoCV(cv=cv, n_jobs=-1)
        model.fit(x, y)
    if False:
        url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/housing.csv'
        data = pd.read_csv(url, header=None).values
        x, y = data[:, :-1], data[:, -1]

    model = Lasso(alpha=.01)
    cv = RepeatedKFold()  # (n_splits=10, n_repeats=3, random_state=42)
    scores = absolute(cross_val_score(model, x_train, y_train,
                                      scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1))
    print('MAE: %.3f (%.3f)' % (mean(scores), std(scores)))
    model.fit(x_train, y_train)

    y_pred = model.predict(x_train)

    matplotlib.use('MacOSX')
    plt.scatter(x_test.attr000, y_test, color='purple', label='actual')
    plt.scatter(x_train.attr000, y_pred, color='cornflowerblue', label='predicted')
    plt.xlabel('data')
    plt.ylabel('target')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

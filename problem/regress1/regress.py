#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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


from pathlib import Path

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn as sns


def report(fspec='~/Desktop/data.csv', pair=False):
    df = (pandas.read_csv(Path(fspec).expanduser())
          .drop('foo', axis=1))
    print(df[0:3])
    ncols = df.shape[1] - 1
    array = df.values
    X = array[:, 0:ncols]
    Y = array[:, ncols]
    find_good_features(X, Y)
    regress(df.median_dom.values.reshape(-1, 1), df.q3_dom.values)
    if pair:
        sns.pairplot(df)


def regress(X, y):
    lr = LinearRegression()
    lr.fit(X, y)
    fig, ax = plt.subplots()
    ax.scatter(y, lr.predict(X), edgecolors=(0, 0, 0))
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()


# https://machinelearningmastery.com/feature-selection-machine-learning-python/
# Feature Extraction with Univariate Statistical Tests
# (Chi-squared for classification)
def find_good_features(X, Y, nfeat=2):
    test = SelectKBest(score_func=chi2, k=nfeat)
    fit = test.fit(X, Y)
    numpy.set_printoptions(precision=3)
    print(fit.scores_)
    features = fit.transform(X)
    print(features[0:nfeat, :])


if __name__ == '__main__':
    report()

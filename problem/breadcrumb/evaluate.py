#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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

import os
import pandas
import sklearn.metrics
import sys

sys.path.append('.'); import cluster


def summarize_location(loc):
    '''Return 0 for "home" locations, 1 for other ("work").'''
    return cluster.place_classifier_predict(*loc)


def predict_destination(src):
    '''If we're currently near home then predict work, or vice versa.'''
    return 1 - cluster.place_classifier_predict(*src)


def evaluate(df, verbose=False):

    src_dst = []
    for i, row in df.iterrows():
        src = row.start_lng, row.start_lat
        dst = row.end_lng, row.end_lat
        src_dst.append((src, dst))

    predictions = []
    actuals = []
    for src, dst in src_dst:
        actuals.append(summarize_location(dst))
        predictions.append(predict_destination(src))

    if verbose:
        print(sklearn.metrics.confusion_matrix(actuals, predictions))

    df_confusion = pandas.crosstab(
        pandas.Series(actuals, name='Actual'),
        pandas.Series(predictions, name='Predicted'))
    print('')
    print(df_confusion)
    print(df_confusion / df_confusion.sum(axis=1))


if __name__ == '__main__':
    os.chdir('/tmp')
    evaluate(pandas.read_csv('trip_summary.csv'))

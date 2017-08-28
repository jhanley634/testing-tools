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

import matplotlib.pyplot as plt
import os
import pandas
import pprint
import sklearn.svm
import sklearn.cluster
import sys

sys.path.append('.'); import peninsula


def approx(n, k=400):
    '''Returns approximately n, that is, discretized to coarser resolution.'''
    return round(n * k) / k


def place_classifier_predict(lng, lat):
    '''Returns 0 for locations near home, 1 for locations near work.'''
    is_near_home = lng > -121.8
    return 0 if is_near_home else 1


def cluster(df, k=2, verbose=False,
            left=-122.25, x_size=.476,
            bottom=37.166, y_size=.372):
    '''Pass in a trip_summary dataframe and desired # of clusters.'''

    for i, row in df.iterrows():
        places.append((row.end_lng, row.end_lat))

    places.sort()
    if verbose:
        pprint.pprint(places)

    est = sklearn.cluster.KMeans(k)
    est.fit(places)

    fig, ax = plt.subplots()
    img = plt.imread('topoquest-peninsula.jpg')
    extent = (left, left + x_size, bottom, bottom + y_size)
    ax.imshow(img, alpha=0.3, extent=extent)
    ax.ticklabel_format(useOffset=False)
    colors = 'red purple blue aqua'.split()

    X = []
    y = []

    for place in places:
        clust_no, = est.predict([place])
        ax.scatter(approx(place[0]), approx(place[1]),
                   color=colors[clust_no], marker='s', linewidth=5)
        X.append(list(place))
        y.append(clust_no)

    for lng, lat in peninsula.cities():
        ax.scatter(lng, lat, color='green')

    plt.savefig('trip_clusters_%d.pdf' % k)
    plt.savefig('trip_clusters_%d.png' % k)
    # plt.show()

    colors = 'salmon darkorchid'.split()
    for place in places:
        clust_no = place_classifier_predict(*place)
        ax.scatter(place[0], place[1],
                   color=colors[clust_no], marker='^')
        if verbose:
            print(clust_no, place)
    print(y)
    plt.show()


if __name__ == '__main__':
    os.chdir('/tmp')
    places = []  # trip sources, or destinations
    cluster(pandas.read_csv('trip_summary.csv'))

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

from sqlalchemy import Table
import collections
import csv
import datetime
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

import problem.breadcrumb.dbcred as dbcred


def cities():
    '''Returns some south-bay landmarks. Coordinates come from wikipedia.'''
    return [
        (-122.0819, 37.38944),  # Mountain View
        (-122.0375, 37.37111),  # Sunnyvale
        (-121.9692, 37.35444),  # Santa Clara
        (-121.9000, 37.33333),  # San Jose
        (-121.8167, 37.30310),  # 101 & El Camino in S.J.
        (-121.8950, 37.43472),  # Milpitas
        (-121.9617, 37.23611),  # Los Gatos
    ]


def get_one(i, coords):
    # Project a sequence of number pairs down to just a sequence of numbers.
    for coord in coords:
        yield coord[i]


def get_x(coords):
    return list(get_one(0, coords))


def get_y(coords):
    return list(get_one(1, coords))


def approx(n, k=400):
    '''Returns approximately n, that is, discretized to coarser resolution.'''
    return round(n * k) / k


def round10(n, k=10):
    '''Round to 1/10ths.'''
    return approx(n, k)


def dow(stamp):
    '''Day of Week, returns 0..6 for Sun..Sat.'''
    return int(stamp.strftime('%w'))


def hour_of_day(stamp):
    return int(stamp.strftime('%H'))  # 0..23


def markup_peninsula_map(sess, wr, c_lng, c_lat, d_lng=.238, d_lat=.186):
    '''Pass in DB session, CSV writer, and center coords of map.'''

    wr.writerow('file_no dow hour_of_day elapsed'
                ' start_lng start_lat end_lng end_lat'.split())

    img = plt.imread('topoquest-peninsula.jpg')
    # Deltas are valid for 1280 sq px map, at 32m/px, near San Jose.
    left, top = c_lng - d_lng, c_lat + d_lat
    right, bottom = c_lng + d_lng, c_lat - d_lat
    extent = (left, right, bottom, top)
    heat = collections.defaultdict(int)

    tp = Table('trip_point_local_journey',
               META, autoload=True, autoload_with=ENGINE)
    file_nos = [file_no
                for file_no, in sess.query('distinct file_no from %s' % tp)]
    for file_no in sorted(file_nos):
        if file_no > 100:
            continue
        print(file_no, end=', ')
        sys.stdout.flush()
        elapsed = 0
        first = last = None
        crumbs = set()  # This will suppress duplicates.
        for row in sess.query(tp).filter(tp.c.file_no == file_no):
            if left < row.lng < right and bottom < row.lat < top:  # in bbox
                crumb = approx(row.lng), approx(row.lat)
                crumbs.add(crumb)
                if first is None:
                    first = crumb
                last = crumb
                elapsed = max(elapsed, row.elapsed)

        crumbs = sorted(crumbs)
        fig, ax = plt.subplots()
        ax.imshow(img, alpha=0.3, extent=extent)
        ax.scatter(get_x(crumbs), get_y(crumbs), marker='.', color='darkblue')
        ax.scatter(get_x(cities()), get_y(cities()), color='green')
        if first:
            stmp = datetime.datetime.utcfromtimestamp(row.stamp.timestamp())
            wr.writerow([file_no,
                         dow(stmp), hour_of_day(stmp), round10(elapsed),
                         first[0], first[1], last[0], last[1]])
            ax.scatter(first[0], first[1], marker='s', color='lime')
            ax.scatter(last[0], last[1], marker='x', color='red')
        ax.ticklabel_format(useOffset=False)  # suppress scientific notation
        plt.savefig('trip_%03d.pdf' % file_no)
        plt.savefig('trip_%03d.png' % file_no)
        plt.close()
        for crumb in crumbs:
            heat[crumb] += 1
    heatmap(heat, left, right - left, bottom, top - bottom)


def heatmap(heat, left, x_size, bottom, y_size, k=300, floor=3):
    # based on https://stackoverflow.com/questions/2369492/generate-a-heatmap
    X, Y = np.meshgrid(np.linspace(left, left + x_size, k),
                       np.linspace(bottom, bottom + y_size, k))
    Z = np.zeros((k, k))

    bright = max(heat.values())
    for lng, lat in cities():
        heat[(approx(lng), approx(lat))] = -1

    for (lng, lat), count in heat.items():
        lng -= left
        lat -= bottom
        count = -bright if count < 0 else max(count, floor)
        Z[int(lat * k / y_size),
          int(lng * k / x_size)] = count
    plt.subplot(111)
    plt.hexbin(X.ravel(),
               Y.ravel(),
               C=Z.ravel(),
               gridsize=60, cmap=cm.cool, bins=None)
    plt.axis([X.min(), X.max(), Y.min(), Y.max()])
    cb = plt.colorbar()
    cb.set_label('grid counts')
    plt.ticklabel_format(useOffset=False)
    plt.savefig('heatmap_of_trips.pdf')
    plt.savefig('heatmap_of_trips.png')


if __name__ == '__main__':
    CONN, ENGINE, META = dbcred.get_cem('breadcrumb')
    os.chdir('/tmp')
    # http://bit.ly/2vtB20t
    # https://www.topoquest.com/map.php?lat=37.35236&lon=-122.01234&datum=nad83
    # USGS Map Name:  Cupertino, CA    Map MRC: 37122C1
    # Map Center:  N37.35236°  W122.01234°    Datum: NAD83    Zoom: 32m/pixel
    with open('trip_summary.csv', 'w') as csvfile:
        markup_peninsula_map(
            dbcred.SESSION, csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL),
            -122.012, 37.352)

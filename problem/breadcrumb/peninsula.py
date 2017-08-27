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
import matplotlib.pyplot as plt
import numpy as np
import os

import dbcred


def get_one(i, coords):
    # Project a sequence of number pairs down to just a sequence of numbers.
    for coord in coords:
        yield coord[i]


def get_x(coords):
    return list(get_one(0, coords))


def get_y(coords):
    return [y for y in get_one(1, coords)]


def markup_peninsula_map(sess):

    img = plt.imread('topoquest-peninsula.jpg')
    left, top = willow_101 = -122.156, 37.471  # the Willow / 101 interchange
    right, bottom = pruneyard_17 = -121.918, 37.285
    bias = 0
    # bias = 100  # This conveniently suppresses scientific notation on x-axis.
    extent = (bias + left, bias + right, bottom, top)
    fig, ax = plt.subplots()
    ax.imshow(img, alpha=0.2, extent=extent)

    crumbs = set()  # This will suppress duplicates.
    tp = Table('trip_point_local_journey',
               META, autoload=True, autoload_with=ENGINE)
    for row in sess.query(tp).filter(tp.c.file_no < 77):
        crumbs.add((row.lng, row.lat))
    ax.scatter(get_x(crumbs), get_y(crumbs), linewidth=1, color='darkblue')

    plt.show()


if __name__ == '__main__':
    CONN, ENGINE, META = dbcred.get_cem('breadcrumb')
    os.chdir('/tmp')
    # http://bit.ly/2wSVY4K
    # https://www.topoquest.com/map.php?lat=37.37826&lon=-122.04088
    # USGS Map Name:  Mountain View, CA    Map MRC: 37122D1
    # Map Center:  N37.37826°  W122.04088°    Datum: NAD27    Zoom: 16m/pixel
    markup_peninsula_map(dbcred.SESSION)

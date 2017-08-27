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
import os

import dbcred


def get_one(i, coords):
    # Project a sequence of number pairs down to just a sequence of numbers.
    for coord in coords:
        yield coord[i]


def get_x(coords):
    return [x for x in get_one(0, coords)]


def get_y(coords):
    return list(get_one(1, coords))


def markup_peninsula_map(sess, c_lng, c_lat, d_lng=.238, d_lat=.186):
    '''Pass in DB session, and center coords of map.'''

    img = plt.imread('topoquest-peninsula.jpg')
    # Deltas are valid for 1280 sq px map, at 32m/px, near San Jose.
    left, top = c_lng - d_lng, c_lat + d_lat
    right, bottom = c_lng + d_lng, c_lat - d_lat
    bias = 0
    # bias = 100  # This conveniently suppresses scientific notation on x-axis.
    extent = (bias + left, bias + right, bottom, top)
    fig, ax = plt.subplots()
    ax.imshow(img, alpha=0.3, extent=extent)

    crumbs = set()  # This will suppress duplicates.
    tp = Table('trip_point_local_journey',
               META, autoload=True, autoload_with=ENGINE)
    file_nos = [file_no
                for file_no, in sess.query('distinct file_no from %s' % tp)]
    for file_no in sorted(file_nos):
        for row in sess.query(tp).filter(tp.c.file_no < file_no):
            if left < row.lng < right and bottom < row.lat < top:  # in bbox
                crumbs.add((row.lng, row.lat))
        crumbs = sorted(crumbs)
        ax.scatter(get_x(crumbs), get_y(crumbs), linewidth=1, color='darkblue')

        print(file_no)
        if (file_no % 5 == 0):
            plt.show()


if __name__ == '__main__':
    CONN, ENGINE, META = dbcred.get_cem('breadcrumb')
    os.chdir('/tmp')
    # http://bit.ly/2vtB20t
    # https://www.topoquest.com/map.php?lat=37.35236&lon=-122.01234&datum=nad83
    # USGS Map Name:  Cupertino, CA    Map MRC: 37122C1
    # Map Center:  N37.35236°  W122.01234°    Datum: NAD83    Zoom: 32m/pixel
    markup_peninsula_map(dbcred.SESSION, -122.012, 37.352)

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


class Xform1:
    '''Models 1-D linear transformation between lng/lat coord and pixels.'''

    def __init__(self, min_coord, max_coord, max_px):
        self.min_coord = min_coord
        self.coord_range = max_coord - min_coord
        self.max_px = max_px
        assert self.coord_range > 0

    def to_px(self, coord_val):
        delta = coord_val - self.min_coord
        assert 0 <= delta <= self.coord_range, delta  # Must stay in bounds.
        return self.max_px * (delta / self.coord_range)


class Xform2:
    '''Models 2-D linear transformation between lng/lat coord and pixels.'''

    def __init__(self, coord_nw, coord_se, width_height_px):
        # NorthWest is upper left and SouthEast is lower right.
        # Those happened to be the locations that were readily measurable.
        # Origin is SouthEast, lower left. Pass in (lng, lat) coordinates.
        self.lng_xform = Xform1(coord_nw[0], coord_se[0], width_height_px[0])
        self.lat_xform = Xform1(coord_se[1], coord_nw[1], width_height_px[1])

    def to_px(self, coord_val):
        lng, lat = coord_val
        return self.lng_xform(lng), self.lat_xform(lat)


def markup_peninsula_map():

    img = plt.imread('topoquest-peninsula.jpg')
    willow_101 = -122.156, 37.471  # the Willow / 101 interchange
    pruneyard_17 = -121.918, 37.285
    extent = (100 + willow_101[0], 100 + pruneyard_17[0],
              pruneyard_17[1], willow_101[1])
    xform = Xform2(willow_101, pruneyard_17,
                   img.shape[:2])  # Shape also mentions 3, # of RGB channels.
    fig, ax = plt.subplots()
    # ax.set_aspect('equal')
    ax.imshow(img, extent=extent)
    print(fig, ax)
    plt.show()


if __name__ == '__main__':
    os.chdir('/tmp')
    # http://bit.ly/2wSVY4K
    # https://www.topoquest.com/map.php?lat=37.37826&lon=-122.04088
    # USGS Map Name:  Mountain View, CA    Map MRC: 37122D1
    # Map Center:  N37.37826°  W122.04088°    Datum: NAD27    Zoom: 16m/pixel
    markup_peninsula_map()

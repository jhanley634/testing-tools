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


def markup_peninsula_map():

    img = plt.imread('topoquest-peninsula.jpg')
    willow_101 = -122.156, 37.471  # the Willow / 101 interchange
    pruneyard_17 = -121.918, 37.285
    extent = (100 + willow_101[0], 100 + pruneyard_17[0],
              pruneyard_17[1], willow_101[1])
    fig, ax = plt.subplots()
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

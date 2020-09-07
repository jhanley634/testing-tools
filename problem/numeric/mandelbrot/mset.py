#! /usr/bin/env python

# Copyright 2020 John Hanley.
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
import sys

import colorbrewer

from problem.numeric.mandelbrot.ppm import PPM

PX_RESOLUTION = int(os.getenv("MSET_PX_RESOLUTION", "100"))  # defaults to 100px square


def mandelbrot_set(xc: float, yc: float, sz: float, fout, cmap):
    """Given center x,y and a "radius" size, create a square PPM m-set."""
    # from https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings
    ppm = PPM(fout, PX_RESOLUTION, cmap=cmap)

    for x0, y0 in ppm.get_points(xc, yc, sz):
        ppm.plot(_cycles_to_escape(x0, y0))


def _cycles_to_escape(x0: float, y0: float, max_iter=255):
    x, y, i = 0.0, 0.0, 0
    while x ** 2 + y ** 2 <= 4 and i < max_iter:
        x, y = (x**2 - y**2 + x0, 2 * x * y + y0)
        i += 1
    return i


if __name__ == '__main__':
    args = map(float, sys.argv[1:])
    cmap = colorbrewer.PRGn[11]
    cmap = None  # greyscale
    mandelbrot_set(*args, sys.stdout, cmap)

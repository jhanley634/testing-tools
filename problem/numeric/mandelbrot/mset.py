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

PX_RESOLUTION = int(os.getenv("MSET_PX_RESOLUTION", "100"))  # defaults to 100px square


class PPM:
    """Implements netpbm ascii Portable Pix Map."""

    def __init__(self, fout, x_px, y_px):
        fout.write("P3\n")  # ppm magic number
        fout.write(f"{x_px} {y_px}\n")
        fout.write("255\n")  # max val, 8-bit channels, 24-bit color
        self.fout = fout
        self.cmap = colorbrewer.PRGn[11]

    def plot(self, grey_value):
        assert 0 <= grey_value < 256, grey_value
        # r, g, b = grey_value, grey_value, grey_value
        r, g, b = self.cmap[grey_value % len(self.cmap)]
        self.fout.write(f"{r} {g} {b}\n")


def _get_points(xc, yc, sz):
    """Generates x, y point for each pixel."""
    step = (2 * sz) / (PX_RESOLUTION - 1)
    for j in range(PX_RESOLUTION):
        for i in range(PX_RESOLUTION):
            yield (
                xc - sz + step * i,
                yc - sz + step * j)


def mandelbrot_set(xc, yc, sz, fout, max_iter=255):
    """Given center x,y and a "radius" size, create a square PPM m-set."""
    # from https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings
    ppm = PPM(fout, PX_RESOLUTION, PX_RESOLUTION)

    for x0, y0 in _get_points(xc, yc, sz):
        x, y, i = 0, 0, 0
        while x * x + y * y <= 4 and i < max_iter:
            x, y = x * x - y * y + x0, 2 * x * y + y0
            i += 1
        ppm.plot(i)


if __name__ == '__main__':
    args = map(float, sys.argv[1:])
    mandelbrot_set(*args, sys.stdout)

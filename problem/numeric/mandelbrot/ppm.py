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

import colorbrewer


class PPM:
    """Implements square netpbm ascii Portable Pix Map."""

    def __init__(self, fout, size_px):
        fout.write("P3\n")  # ppm magic number
        fout.write(f"{size_px} {size_px}\n")
        fout.write("255\n")  # max val, 8-bit channels, 24-bit color
        self.fout = fout
        self.size_px = size_px
        self.cmap = colorbrewer.PRGn[11]

    def plot(self, grey_value):
        assert 0 <= grey_value < 256, grey_value
        # r, g, b = grey_value, grey_value, grey_value
        r, g, b = self.cmap[grey_value % len(self.cmap)]
        self.fout.write(f"{r} {g} {b}\n")

    def get_points(self, xc, yc, sz):
        """Generates x, y point for each pixel.
        Maps from pixel space to continuous space."""
        step = (2 * sz) / (self.size_px - 1)
        for j in range(self.size_px):
            for i in range(self.size_px):
                yield (
                    xc - sz + step * i,
                    yc - sz + step * j)

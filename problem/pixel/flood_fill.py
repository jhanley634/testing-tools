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

import unittest
import sys
sys.path.append('.'); from line_draw import Canvas


class FloodFiller:

    def __init__(self, canvas):
        self.canvas = canvas
        self.n_regions = 0  # No regions filled, so far.
        self.pending = []

    def fill(self, x, y, color=None):

        if color is None:
            color = chr(ord('0') + self.n_regions)
        self.n_regions += 1
        self._fill(x, y, color)

    def _fill(self, x, y, color):

        cur_color = self.canvas.color_at(x, y)
        is_valid = self.canvas.is_empty(x, y) or cur_color == color
        assert is_valid, (x, y, cur_color)
        self.canvas.point(x, y, color=color)

        for x, y in self._neighborhood(x, y):
            if self.canvas.is_empty(x, y):
                self.canvas.point(x, y, color=color)
                self.pending.append((x, y))

        while len(self.pending) > 0:
            x, y = self.pending.pop()
            self._fill(x, y, color)

    NON_VON_OFFSETS = [(-1, -1), (0, -1), (1, -1),
                       (-1, 0), (1, 0),
                       (-1, 1), (0, 1), (1, 1)]

    # The 4 cardinal directions describe a von Neumann neighborhood.
    OFFSETS = [(0, -1),
               (-1, 0), (1, 0),
               (0, 1)]

    def _neighborhood(self, x, y):
        for x_off, y_off in FloodFiller.OFFSETS:
            xx, yy = x + x_off, y + y_off
            if self.canvas.is_in_bounds(xx, yy):
                yield xx, yy


class FloodTest(unittest.TestCase):

    def test0(self):
        self.assertEqual(8, len(FloodFiller.NON_VON_OFFSETS))

    def test1(self):
        filler = FloodFiller(Canvas(16))
        c = filler.canvas
        for r in range(42):
            c.circle((0, 0), 14 + r / 20.0)
        self.assertEqual(279, c.num_points())

        filler.fill(4, 4)
        self.assertEqual(812, c.num_points())

        with open('/tmp/canvas.txt', 'w') as fout:
            fout.write(str(c) + '\n')


if __name__ == '__main__':
    unittest.main()

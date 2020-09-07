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

import numpy as np


class Canvas:
    '''Models a grid one can draw pixels on, with positive Y at top.'''

    BG_INK = set(' .o-|/')  # Background ink colors for axes, rather than app.

    def __init__(self, size):
        '''In the lower left, (-size, -size) is first invalid pixel.'''

        def draw_axes():
            for x in self._range():
                for y in self._range():
                    self.point(x, y, ' ')
                    if (x % 2 == 0
                            and y % 2 == 0):
                        self.point(x, y, '.')
            for x in self._range():
                self.point(x, 0, '-')
            for y in self._range():
                self.point(0, y, '|')
            self.point(0, 0, 'o')

        self.size = size
        s = 2 * size - 1
        self.grid = np.zeros((s, s), dtype='U1')
        draw_axes()

    def num_points(self):
        return sum(0 if c in Canvas.BG_INK else 1
                   for c in self.grid.flatten())
        # return sum([0 if self.grid[self._coord(x, y)] in Canvas.BG_INK else 1
        #             for x in self._range()
        #             for y in self._range()])

    def __str__(self):

        def wider(text):
            for ch in text:
                yield ch
                # yield ch  # Optionally make aspect ratio twice as wide.

        def line(y):
            return ''.join(wider([self.grid[self._coord(x, y)]
                                  for x in self._range()]))
        return '\n'.join([line(-y)
                          for y in self._range()])

    def _range(self):
        '''Iterates from one side of canvas to the other.'''
        return range(-(self.size - 1), self.size)

    def _coord(self, x, y):
        return int(self.size - 1 + x), int(self.size - 1 + y)

    def point(self, x, y, color='X'):
        '''Draw a single point.'''
        assert x < self.size, x
        assert y < self.size, y
        self.grid[self._coord(x, y)] = color

    def is_in_bounds(self, x, y):
        size = self.size
        return (True
                and -size < x < size
                and -size < y < size)

    def color_at(self, x, y):
        return self.grid[self._coord(x, y)]

    def is_empty(self, x, y):
        return self.color_at(x, y) in Canvas.BG_INK

    def line(self, point0, point1, color='X'):
        '''Draw a line between two points.'''

        def div(a, b, epsilon=1e-3):
            '''Divides a by b, while avoiding div-by-zero error.'''
            return a / (b if abs(b) > epsilon else epsilon)

        def range_(delta):
            '''Iterates from point0 up to but not including point1.'''
            if delta > 0:
                return range(int(delta))
            else:
                return range(int(delta + 1), 1)  # Reduce delta by 1, visit 0.

        (x0, y0), (x1, y1) = point0, point1
        delta_x = x1 - x0
        delta_y = y1 - y0
        if abs(delta_x) > abs(delta_y):
            m = div(delta_y, delta_x)  # Slope is a signed quantity.
            assert m <= 1
            for i in range_(delta_x):
                self.point(x0 + i, y0 + m * i, color)
        else:
            im = div(delta_x, delta_y)  # Inverse slope, 1/m.
            assert im <= 1
            for i in range_(delta_y):
                self.point(x0 + im * i, y0 + i, color)

    def circle(self, center_point, r, color='c'):
        '''https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example'''
        x0, y0 = center_point
        x = r - 1
        y = 0
        dx = dy = 1
        err = dx - 2 * r

        while x >= y:
            for x_off, y_off in [(x, y), (y, x), (-y, x), (-x, y),
                                 (-x, -y), (-y, -x), (y, -x), (x, -y)]:
                self.point(x0 + x_off, y0 + y_off, color=color)
            if err <= 0:
                y += 1
                err += dy
                dy += 2
            if err > 0:
                x -= 1
                dx += 2
                err += -2 * r + dx


def gcd(a, b):
    '''
    en.wikipedia.org/wiki/Greatest_common_divisor#Using_Euclid.27s_algorithm
    '''
    assert a > 0, a  # Pass in positive integers, please.
    assert b > 0, b
    if a == b:
        return a
    if a > b:
        return gcd(a - b, b)
    else:
        return gcd(a, b - a)


class CanvasTest(unittest.TestCase):

    def test_gcd(self):  # Not related to canvas at this point.

        def check(expect, nums):  # Check that Euclid works fine both ways.
            m, n = nums
            self.assertEqual(expect, gcd(m, n))
            self.assertEqual(expect, gcd(n, m))

        check(1, (7, 13))
        check(2, (14, 26))
        check(6, (24, 42.0))

    def test_canvas(self):
        c = Canvas(6 + 12)
        self.assertFalse(c.is_in_bounds(c.size, c.size))
        self.assertTrue(c.is_in_bounds(0, 0))
        self.assertTrue(c.is_empty(0, 0))
        self.assertEqual('o', c.color_at(0, 0))
        self.assertEqual(0, c.num_points())

        c.line((0, 0), (0, -4), color='!')
        self.assertEqual(4, c.num_points())

        c.line((0, 0), (-2, 5.6), color='x')
        self.assertEqual(8, c.num_points())

        c.line((0, 0), (5, 2))
        self.assertEqual(12, c.num_points())

        c.line((4, -4), (1, -1), color='\\')
        self.assertEqual(15, c.num_points())

        for r in range(42):
            c.circle((0, 0), 16 + r / 20.0)
        self.assertEqual(339, c.num_points())

        with open('/tmp/canvas.txt', 'w') as fout:
            fout.write(str(c) + '\n')


if __name__ == '__main__':
    unittest.main()

#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

"""Compares numpy running times against python interpreter.
"""

import os
import timeit
import unittest

import PIL.Image
import PIL.ImageColor
import PIL.ImageDraw2
import numpy as np


def get_marked_image(mark_coord=None, radius=20, im_size=(200, 100)):
    if mark_coord is None:
        mark_coord = (20, 10)
    x0, y0 = mark_coord
    box = (x0, y0, x0 + radius, y0 + radius)
    pen = PIL.ImageDraw2.Pen('steelblue', width=9)
    im = PIL.Image.new('RGBA', im_size)
    draw = PIL.ImageDraw2.Draw(im)
    draw.ellipse(box, pen)
    return im


class BboxFinder:

    @staticmethod
    def _find_first_positive(vals, reverse=False):
        start = 0
        sgn = 1
        if reverse:
            start = len(vals) - 1
            sgn = -1
            vals = reversed(vals)

        for i, val in enumerate(vals):
            if val > 0:
                return start + sgn * i
        return start + sgn * i

    @classmethod
    def find_bbox(cls, im):
        pix = np.array(im.convert('L'))  # one-byte greyscale
        col_sums = pix.sum(axis=0)
        row_sums = pix.sum(axis=1)
        assert len(col_sums) == im.width
        assert len(row_sums) == im.height
        x0 = cls._find_first_positive(col_sums)
        x1 = cls._find_first_positive(col_sums, reverse=True)
        y0 = cls._find_first_positive(row_sums)
        y1 = cls._find_first_positive(row_sums, reverse=True)
        return (x0, y0, x1, y1)


class BboxFinderTest(unittest.TestCase):

    @staticmethod
    def _find1():
        im = get_marked_image()
        return BboxFinder.find_bbox(im)

    def test_bbox_finder(self):
        im = get_marked_image()
        im.save(os.path.expanduser('~/Desktop/t.png'))
        # bbox = BboxFinder.find_bbox(im)
        # t = timeit.Timer(self._find1).autorange()
        elapsed = timeit.timeit(self._find1, number=1000)
        self.assertLess(.80, elapsed)
        self.assertLess(elapsed, .99)

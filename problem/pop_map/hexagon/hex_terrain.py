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


"""Implements a "flat" hex grid, using invaluable advice from Amit Patel
https://www.redblobgames.com/grids/hexagons
"""
# We choose flat-top rather than pointy-top hexes,
# with odd-q vertical layout, and axial coords for storage.
# We adopt Amit's "origin at upper left" convention,
# which implies that angles resemble compass angles,
# with small positive angles in quadrant IV rather than I.

from enum import Enum, auto

import numpy as np

from problem.pop_map.hexagon.redblobhex import OffsetCoord, Hex, Point


class Direction(Enum):
    # (col, row) deltas
    SE = (1, 0)
    SOUTH = (0, 1)
    SW = (-1, 0)
    NW = (-1, -1)
    NORTH = (0, -1)
    NE = (1, -1)


class CellContent(Enum):
    # breadcrumbs for a traversed path:
    MARKED_SE = auto()
    MARKED_SOUTH = auto()
    MARKED_SW = auto()
    MARKED_NW = auto()
    MARKED_NORTH = auto()
    MARKED_NE = auto()

    UNMARKED = auto()  # like Path in a maze
    CITY = auto()  # a goal cell
    MOUNTAIN = auto()  # impassable, like Wall in a maz


CELL_GLYPH = 'ZeswWNE.cM'


def cube_to_oddq(cube):
    # from Amit
    col = cube.x
    row = cube.z + (cube.x - (cube.x & 1)) // 2
    return OffsetCoord(col, row)


def oddq_to_cube(hex):
    # from Amit
    x = hex.col
    z = hex.row - (hex.col - (hex.col & 1)) // 2
    y = -x - z
    return Hex(x, y, z)


class HexTerrain:

    def __init__(self):
        self.width = 10
        self.height = 4
        self.cell = np.zeros((self.width * 2, self.height), int)
        self.cell[:][:] = CellContent.UNMARKED.value

    def _q_r_to_x_y(self, q, r) -> tuple:
        """Maps col, row hexagon to x, y numpy storage cell."""
        offset = self.width
        return ()

    def __str__(self):
        s = []
        for row in range(self.height):
            print(row,
                  self.cell[0, row],
                  self.cell[1, row])
            print(CELL_GLYPH[self.cell[0, row]])
            s.append(''.join(CELL_GLYPH[self.cell[col, row]]
                             for col in range(self.width)))
        return '\n'.join(s)


class Car:

    def __init__(self, terr: HexTerrain, x=1, y=1):
        self.terr = terr
        self.loc = Point(x, y)


if __name__ == '__main__':
    print(CellContent.MARKED_SE.value)
    terr = HexTerrain()
    print(terr)

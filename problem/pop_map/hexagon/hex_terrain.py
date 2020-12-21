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
    SOUTH = (0, -1)
    SW = (-1, 0)
    NW = (-1, 1)
    NORTH = (0, 1)
    NE = (1, 1)


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

    def __init__(self, width=10, height=6):
        self.width = width
        self.height = height
        self._cell = np.zeros((self.height, self.width * 1), int)
        self._cell[:][:] = CellContent.UNMARKED.value

    def _q_r_to_x_y(self, q, r) -> tuple:
        """Maps col, row hexagon to x, y numpy storage cell."""
        offset = self.width
        return ()

    def plot(self, loc: Point, color=CellContent.MARKED_NORTH.value):
        q, r = loc.x, loc.y
        self._cell[r, q] = color

    def is_passable(self, loc: Point):
        q, r = loc.x, loc.y
        return self._cell[r, q] not in (
            CellContent.MOUNTAIN.value,  # impassable
            CellContent.CITY.value,      # end of journey
        )

    def is_goal(self, loc: Point):
        q, r = loc.x, loc.y
        return self._cell[r, q] == CellContent.CITY.value  # end of journey

    def _glyph(self, col, row):
        if col < 0:
            return str(row % 10)
        if not (0 <= row < self.height):
            return str(col % 10)
        assert 0 <= col < self.width, col
        assert 0 <= row < self.height, row
        return CELL_GLYPH[self._cell[row, col]]

    def display(self):
        rows = ['' for _ in range(self.height * 4)]
        for row in range(self.height):
            for col in range(0, self.width, 2):
                q, r = col, row
                v1 = self._glyph(q + 1, r - 1)
                v2 = self._glyph(q + 0, r)
                v3 = self._glyph(q + 1, r)
                start = 4 * (self.height - row - 1)
                rows[start + 0] += r' /   \  3 '.replace('3', v3)
                rows[start + 1] += r'/  2  \___'.replace('2', v2)
                rows[start + 2] += r'\ : : /   '
                rows[start + 3] += r' \___/ 1  '.replace('1', v1)
        return '\n'.join(rows)

    def __str__(self):
        print(self.display())
        s = []
        for row in range(self.height - 1, -1, -1):
            s.append(''.join(CELL_GLYPH[self._cell[row, col]]
                             for col in range(self.width)))
        return '\n'.join(s)


class Truck:

    def __init__(self,
                 terr: HexTerrain,
                 x=1, y=1,
                 direction=Direction.NORTH):
        self._terr = terr
        self._loc = Point(x, y)
        self._terr.plot(self._loc)
        self._direction = direction

    def steer(self, direction: Direction):
        self._direction = direction

    def move(self, distance=1):
        dir_idx = list(Direction).index(self._direction)
        dx, dy = self._direction.value
        for i in range(distance):
            new_x = self._loc.x + dx
            new_y = self._loc.y + dy
            if self._terr.is_passable(Point(new_x, new_y)):
                print(self._direction.value, self._direction)
                self._loc = Point(new_x, new_y)
                self._terr.plot(self._loc, 1 + dir_idx)


if __name__ == '__main__':
    truck = Truck(HexTerrain(), x=0)

    truck.steer(Direction.NORTH)
    truck.move(1)
    # truck._loc = Point(1, 1)
    # truck._terr.plot(truck._loc)
    # truck.move(1)

    truck.steer(Direction.NE)
    truck.move(2)

    truck.steer(Direction.SOUTH)
    truck.move(2)

    truck.steer(Direction.NE)
    truck.move(2)

    truck.steer(Direction.SE)
    truck.move(3)

    print(truck._terr)

#! /usr/bin/env python

from collections import namedtuple
from operator import itemgetter
from typing import List
import random

import numpy as np


Voxel = namedtuple('Voxel', 'x y z')


class Voxels:
    """Turns text input into a list of Voxels."""

    def __init__(self, text: str):
        depth = 1 + int(max(text))
        lines = text.splitlines()
        height = len(lines)
        width = max(map(len, lines))
        self.model = np.zeros((width, height, depth), int)
        voxels = []
        for j, line in enumerate(lines):
            y = len(lines) - j  # Origin is at lower left.
            for x, ch in enumerate(line):
                if ch.isnumeric():  # We ignore ocean pixels.
                    assert ch > '0', (ch, line)
                    for z in range(1, int(ch) + 1):
                        voxel = Voxel(x, y, z)
                        self.model[voxel] = True
                        voxels.append(voxel)
        random.shuffle(voxels)
        self.voxels = voxels

    def render(self) -> str:
        for voxel in self.voxels:
            assert self.model[voxel], voxel
        width, height, depth = self.model.shape
        return '\n'.join(self._raster(height - 1 - y)  # origin LL
                         for y in range(height))

    def _raster(self, y) -> str:
        width = self.model.shape[0]
        return ''.join(self._depth_val(x, y)
                       for x in range(width))

    def _depth_val(self, x, y) -> str:
        """Returns blank for ocean, or 1..3 for coast..mountain."""
        depth = self.model.shape[2]
        val = ' '  # Ocean, by default.
        for z in range(depth):
            if self.model[(x, y, z)]:
                val = str(z)
        return val


def three_d_print(voxels: List[Voxel]) -> str:
    out = _get_zeros(voxels)
    cur = voxels[0]  # 3-D print head position
    elapsed = 0  # Zero cost to move print head to initial voxel.
    for voxel in voxels:
        _verify_feasible(out, *voxel)
        out[voxel] = True
        elapsed += _manhattan_distance(cur, voxel)
    return elapsed, out


def _get_zeros(voxels: List[Voxel]):
    assert len(voxels)
    width = 1 + max(map(itemgetter(0), voxels))
    height = 1 + max(map(itemgetter(1), voxels))
    depth = 1 + max(map(itemgetter(2), voxels))
    return np.zeros((width, height, depth), int)


def _manhattan_distance(a: Voxel, b: Voxel) -> int:
    return (abs(a.x - b.x)
            + abs(a.y - b.y)
            + abs(a.z - b.z))


def _verify_feasible(out, x, y, z):
    """Ensure there is a foundation to print a mountain top upon."""
    for z1 in range(1, z):
        if not out[(x, y, z1)]:
            raise ValueError(f'No support for ({x}, {y}, {z})')


islands = Voxels("""
                  1
    111          1121
 1112211       11223211
1112233211      112321
  122211          13
    1211    1      1                         11
     1     1211                             12321
          1123211                            121
           1121                               1
            11
""")


def xyz(coord):
    return coord


def yxz(coord):
    return (coord.y,
            coord.x,
            coord.z)


def zxy(coord):
    return (coord.z,
            coord.x,
            coord.y)


def zyx(coord):
    return tuple(reversed(coord))


n1, out1 = three_d_print(sorted(islands.voxels, key=xyz))
n2, out2 = three_d_print(sorted(islands.voxels, key=zxy))
n3, out3 = three_d_print(sorted(islands.voxels, key=zyx))
n4, out4 = three_d_print(sorted(islands.voxels, key=yxz))
print(n1, n2, n3, n4,
      np.array_equal(out1, out2),
      np.array_equal(out1, out3),
      np.array_equal(out1, out4))
# print(three_d_print(islands.voxels)[0])  # fails due to No Support

# volcanic voxels
#
# Some volcanic islands are depicted above.
# A 3-D printer will create a model of them.
# The input of (x, y, z) voxels is now in a randomly permuted order.
# Write a function that puts the voxels in "better than naïve" order.

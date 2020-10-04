#! /usr/bin/env python

from collections import namedtuple
import random

import numpy as np


Voxel = namedtuple('Voxel', 'x y z')


class VoxelReader:
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


islands = VoxelReader("""
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
print(islands.render())

# volcanic voxels
#
# Some volcanic islands are depicted below.
# A 3-D printer will create a model of them.
# The input of (x, y, z) voxels is now in a randomly permuted order.
# Write a function that puts the voxels in "better than naïve" order.

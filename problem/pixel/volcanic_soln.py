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

import numpy as np

import pixel.volcanic_voxels as vv


class IslandFinder:
    """Labels each isolated clump of voxels."""

    # This is the von Neumann neighborhood in 3-space.
    NBR_DIRS = list(map(np.array, [
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    ]))

    def __init__(self, islands: vv.Voxels):
        self.islands = islands
        self.label = self._get_label()
        self.cur_label = ord('A')
        while self._add_labels():
            pass
        self.rename = self._find_min_labels()

    def _get_label(self):
        label = np.zeros(self.islands.model.shape, int)
        label_val = 1
        for voxel in self.islands.voxels:
            label[voxel] = label_val
            label_val += 1
        return label

    def _add_labels(self):
        # w, h, d = self.islands.model.shape
        num_changes = 0
        voxels = set(self.islands.voxels)
        for voxel in sorted(voxels):
            v_val = self.label[voxel]
            vxl = np.array(voxel)
            for dxyz in self.NBR_DIRS:
                nbr = tuple(vxl + dxyz)
                if nbr in voxels:
                    assert 1 == self.islands.model[nbr]
                    n_val = self.label[nbr]
                    if v_val != n_val:
                        self.label[voxel] = min(v_val, n_val)
                        self.label[nbr] = min(v_val, n_val)
                        num_changes += 1
        return num_changes

    def _find_min_labels(self):
        # Turns e.g. {4, 4, 4, 9, 9} into {4: 'A', 9: 'B'}
        vals = set(self.label[voxel]
                   for voxel in self.islands.voxels)
        rename = {}
        name = ord('A')
        for val in sorted(vals):
            rename[val] = chr(name)
            name += 1
        return rename

    def render(self):
        height = self.label.shape[1]
        return '\n'.join(self._raster(height - 1 - y)
                         for y in range(height))

    def _raster(self, y):
        width = self.label.shape[0]
        return ''.join(self._cell(x, y)
                       for x in range(width))

    def _cell(self, x, y):
        val = self.label[vv.Voxel(x, y, 1)]
        if val:
            return self.rename[val]
        else:
            return '.'  # ocean

    def three_d_print_elapsed_time(self):
        def _key(voxel):
            val = self.label[tuple(voxel)]
            assert val, voxel
            return (self.rename[val],) + voxel

        voxels = sorted(self.islands.voxels, key=_key)
        pm = vv.PrintedModel(voxels)
        return pm.elapsed


print(IslandFinder(vv.islands).render())
print(IslandFinder(vv.islands).three_d_print_elapsed_time())

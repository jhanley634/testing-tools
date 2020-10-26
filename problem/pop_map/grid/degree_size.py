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

from decimal import Decimal

from geopy.distance import distance
import geopy


def step_size():
    # https://en.wikipedia.org/wiki/St._Louis_Lambert_International_Airport
    stl = geopy.Point(38.747222, -90.361389)  # population midpoint
    one_grid = distance(miles=64)
    north = one_grid.destination(stl, bearing=0)
    east = one_grid.destination(stl, bearing=90)
    lat_step = north.latitude - stl.latitude
    lng_step = east.longitude - stl.longitude
    return map(_round2, (Decimal(f'{lat_step}'), lng_step))


def _round2(n):
    """Rounds to nearest hundredths."""
    return round(n, 2)

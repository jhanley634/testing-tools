#! /usr/bin/env python

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

import unittest

from boltons.iterutils import frange
from geopy.distance import geodesic
import geopy


def get_circle_of_weighted_points(
        center, distance_m=1000, weight=1, num_points=1000):
    dist = geopy.distance.GeodesicDistance(meters=distance_m)
    return [(weight, dist.destination(point=center, bearing=b))
            for b in frange(0, 360, 360 / num_points)]


def get_center(weighted_points):
    n = len(weighted_points)
    assert n >= 1
    mid = int(n / 2)
    wt, center = sorted(weighted_points, key=compare_weighted_points)[mid]
    total_wt = 0
    lat_disp = 0  # Total (signed) displacement from center in Y direction.
    lng_disp = 0
    for wt, point in weighted_points:
        total_wt += wt
        lat_disp += wt * (point.latitude - center.latitude)
        lng_disp += wt * (point.longitude - center.longitude)

    return geopy.Point(center.latitude + lat_disp / total_wt,
                       center.longitude + lng_disp / total_wt)


def compare_weighted_points(wp):
    wt, pt = wp
    return (wt, pt.latitude, pt.longitude)
    # NB: we care more about latitude, since distance on a parallel shows
    # a sin(lat) scaling effect, while dist. on a meridian has constant scale.


class GridProjectionTest(unittest.TestCase):

    def test_distance(self):
        newport_ri = (41.490080, -71.312796)
        cleveland_oh = (41.499498, -81.695391)
        meters = round(geodesic(newport_ri, cleveland_oh).meters, 1)
        self.assertEqual(866455.4, meters)

    def test_projection(self):
        center = st_louis_mo = geopy.Point(38.627222, -90.197778)
        weighted_points = get_circle_of_weighted_points(center, 20_000)
        error = st_louis_mo.latitude - get_center(weighted_points).latitude
        self.assertEqual(.000114, round(error, 6))  # Answer drifted south.


if __name__ == '__main__':
    unittest.main()

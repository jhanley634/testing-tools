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

from operator import itemgetter
import json
import os

from geopy.distance import distance
from tspy import TSP
import numpy as np

from problem.nearby_zips.tsp.travel_map import parse_addresses


def _dist(loc1, loc2):
    return round(distance(loc1, loc2).meters, 2)  # cm resolution


class PlaceGroup:
    """Models a collection of places (or, in TSP parlance, cities)."""

    def __init__(self):
        self.places_with_description = self._get_places()
        locs = [loc for loc, _ in self.places_with_description]
        bb_s, bb_w = self._find_origin(locs)
        self.locs = [(_dist((lat, lng), (bb_s, lng)), _dist((lat, lng), (lat, bb_w)))
                     for lat, lng in locs]

    def _get_places(self, infile='/tmp/addrs.txt'):
        if not os.path.exists(self._json_filename(infile)):
            with open(infile) as fin:
                places = [(loc, addr) for loc, addr, details in parse_addresses(fin)]
                with open(self._json_filename(infile), 'w') as fout:
                    json.dump(places, fout, indent=2)
        with open(self._json_filename(infile)) as fin:
            return json.load(fin)

    @staticmethod
    def _json_filename(txt_filename):
        return txt_filename.replace('.txt', '.json')

    @staticmethod
    def _find_origin(locs):
        bb_s = min(map(itemgetter(0), locs))  # lat
        bb_w = min(map(itemgetter(1), locs))  # lng
        return bb_s, bb_w


def traveling_salesman():
    pg = PlaceGroup()
    tsp = TSP()
    tsp.read_data(np.array(pg.locs))


if __name__ == '__main__':
    traveling_salesman()

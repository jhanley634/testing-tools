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

import os
import unittest

import simplekml

import dbcred


def explore():
    # from https://stackoverflow.com/questions/15691525/mapnik-example
    bbox = [37.2, 37.6, -122.7, -121.5]
    coords = [(bbox[i], bbox[j])
              for i, j in [(0, 2), (0, 3), (1, 2), (1, 3)]]
    kml = simplekml.Kml()
    for i, coord in enumerate(coords):
        kml.newpoint(name='point %s' % i, coords=[coord])

    kml.save('bbox.kml')


class ExploreGpsBreadcrumbsTest(unittest.TestCase):

    def test_geographic_bounding_box(self):
        road_trips = '(38, 77, 93, 89)'  # Relatively far-ranging journeys.
        # Though trip 89 was most extensive, trips 55 & 59 were longer.
        for extreme, dimension in [
                ('min', 'lng'), ('max', 'lng'), ('min', 'lat'), ('max', 'lat'),
        ]:
            query = ('select round(%s(%s), 1)  from trip_point  where'
                     ' not file_no in %s' % (extreme, dimension, road_trips))
            self.assertIn(result1(query), [-122.4, -121.8, 37.3, 37.5])

    def test_speed_conversion(self):
        self.assertEqual(55, round(to_mph(24.6)))

    def test_max_speed(self):
        # Trip 38 has values in the 80's and 90's, and exactly 100, as well.
        # Trip 72 has a value of 94.6485 (210 mph).
        # Trip 73 lists values as high as 82.72.
        # Trips 77, 83, & 89 list highs of 107.9, 180.0, and 599.6.
        # select file_no, round(max(speed), 1)  from trip_point
        #   group by file_no  having max(speed) > 33;
        # I can believe you drove 77 mph, but 1340 mph is due to an artifact.
        corrupt_trips = '(38, 72, 73, 77, 83, 89, 93)'
        query = ('select max(speed)  from trip_point'
                 '  where not file_no in ' + corrupt_trips)
        self.assertEqual(77, round(to_mph(result1(query))))


def result1(query):
    '''Run a query that produces a single 1-column result.'''
    return result_single_row(query)[0]


def result_single_row(query):
    '''Run a query that produces a single row result.'''
    ret = None
    for row in CONN.execute(query):
        ret = row
    return ret


def to_mph(meter_per_sec):
    return meter_per_sec * 2.236936


if __name__ == '__main__':
    CONN, ENGINE, META = dbcred.get_cem('breadcrumb')
    os.chdir('/tmp')
    explore()
    unittest.main()

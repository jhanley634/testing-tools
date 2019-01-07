#! /usr/bin/env python

# Copyright 2019 John Hanley.
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

import uszipcode

from problem.pop_map.model import query_by_state


class TestModel(unittest.TestCase):

    def test_uszipcode_menlo_park(self, zipcode=94025):
        zse = uszipcode.SearchEngine()
        r = zse.by_zipcode(zipcode)
        self.assertEqual(3448, r.population_density)
        self.assertEqual(115444, r.median_household_income)
        self.assertEqual(16271, r.housing_units)
        self.assertEqual(15388, r.occupied_housing_units)
        self.assertEqual(1000001, r.median_home_value)

    def test_query_by_state(self):
        rows = list(query_by_state('CA'))
        self.assertEqual(1513, len(rows))

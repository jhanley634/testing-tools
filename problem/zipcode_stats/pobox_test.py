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

from uszipcode import SearchEngine, ZipcodeType


class PoboxTest(unittest.TestCase):

    @staticmethod
    def _get_zips(simple_zipcode_results):
        return sorted([int(r.zipcode) for r in simple_zipcode_results])

    def setUp(self):
        self.se = SearchEngine()

    def test_pobox(self):
        r = self.se.by_zipcode(94037)
        self.assertEqual('PO Box', r.zipcode_type)
        self.assertEqual('San Mateo County', r.county)

        self.assertEqual([94037],
                         self._get_zips(self.se.by_city_and_state(
                             'Montara', 'CA', zipcode_type=ZipcodeType.PO_Box)))
        self.assertEqual([94302, 94309],
                         self._get_zips(self.se.by_city_and_state(
                             'Palo Alto', 'CA', zipcode_type=ZipcodeType.PO_Box)))
        self.assertEqual([94119, 94120, 94125, 94126, 94140],
                         self._get_zips(self.se.by_city(
                             'San Francisco', zipcode_type=ZipcodeType.PO_Box)))

    def test_standard(self):
        r = self.se.by_zipcode(94025)
        self.assertEqual('Standard', r.zipcode_type)

        self.assertEqual([94301, 94303, 94304, 94306],
                         self._get_zips(self.se.by_city_and_state('Palo Alto', 'CA')))

    def test_unique(self):
        self.assertEqual([94106, 94135, 94136, 94137, 94138],
                         self._get_zips(self.se.by_city_and_state(
                             'San Francisco', 'CA', zipcode_type=ZipcodeType.Unique)))


if __name__ == '__main__':
    unittest.main()

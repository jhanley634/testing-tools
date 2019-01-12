#! /usr/bin/env python

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

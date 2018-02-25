#! /usr/bin/env python3

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

"""Finds demographic statistics based on zipcode.
"""
import unittest

import uszipcode


class ZipcodeStats:

    def __init__(self):
        self.zse = uszipcode.ZipcodeSearchEngine()

    def get_city_state(self, zipcode):
        r = self.zse.by_zipcode(zipcode)
        return '{} {}'.format(r['City'], r['State'])


class ZipcodeStatsTest(unittest.TestCase):

    def setUp(self):
        self.zc = ZipcodeStats()

    def test_city_state(self):
        self.assertEqual('Beverly Hills CA', self.zc.get_city_state('90210'))


if __name__ == '__main__':
    unittest.main()

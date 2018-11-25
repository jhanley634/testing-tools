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

import quantities as pq
import unittest


class UnitsTest(unittest.TestCase):

    def setUp(self):
        self.apple = pq.UnitQuantity('apple')
        self.orange = pq.UnitQuantity('orange')

    def test_apples_and_oranges(self):
        basket1 = 4 * self.apple
        basket2 = 3 * self.orange
        basket2 += 1 * self.orange
        self.assertNotEqual(basket1, basket2)
        self.assertEqual(int(basket1), int(basket2))

    def test_incompatible_addition(self):
        basket1 = 4 * self.apple
        basket2 = 3 * self.orange
        with self.assertRaises(ValueError):
            basket1 + basket2


if __name__ == '__main__':
    unittest.main()

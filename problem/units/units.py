#! /usr/bin/env python3

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
            basket3 = basket1 + basket2


if __name__ == '__main__':
    unittest.main()

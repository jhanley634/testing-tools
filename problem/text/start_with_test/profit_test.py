
import unittest


def find_profit_quadratic(prices):
    profit = 0
    for i, buy in enumerate(prices):
        for j in range(i, len(prices)):
            sell = prices[j]
            profit = max(profit, sell - buy)
    return profit


def find_profit(prices):
    buy = min(prices)
    del prices[:prices.index(buy)]
    sell = max(prices)
    return sell - buy


class ProfitTest(unittest.TestCase):

    def test_profit(self):
        prices = [12, 10, 15]
        self.assertEqual(5, find_profit_quadratic(prices))
        self.assertEqual(5, find_profit(prices))

    def test_profits(self):
        for expected, prices in [
            (5, [12, 10, 15]),
            (5, [12, 10, 11, 15, 14]),
            (0, [15, 14, 12, 12, 12]),
            (0, [12]),
        ]:
            for fn in [find_profit,
                       find_profit_quadratic]:

                self.assertEqual(expected, fn(prices))

import math
math.sqrt()

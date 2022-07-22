#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
import unittest


class NewsTest(unittest.TestCase):

    def test_news(self):
        xs = [0.0, 0.2, 0.33, 0.43, 0.63, 0.66, 1.0]
        ys = [0.0, 0.25, 0.25, 0.5, 0.5, 1.0, 1.0]
        self.assertEqual(.5575, solution(xs, ys))


def hypo_news():
    pass


def solution(x, y):
    assert 2 <= len(x) <= 100
    assert len(x) == len(y)
    for xi, yi in zip(x, y):
        assert 0 <= xi <= 1
        assert 0 <= yi <= 1
    assert len(set(x)) == len(x)
    assert x == sorted(x)
    assert y == sorted(y)
    p0 = x[0], y[0]
    p_final = x[-1], y[-1]
    assert p0 == (0, 0)
    assert p_final == (1, 1)

    return area_under_curve(x, y)


def area_under_curve(x, y):
    """Find area under curve as a sum of trapezoids.

    Reference: https://en.wikipedia.org/wiki/Trapezoidal_rule
    """
    area = 0
    for i in range(1, len(x)):
        area += (x[i] - x[i - 1]) * .5 * (y[i - 1] + y[i])
    return area


if __name__ == '__main__':
    hypo_news()
    unittest.main(exit=False)
    print(solution([0, .5, 1],
                   [0, .25, 1]))

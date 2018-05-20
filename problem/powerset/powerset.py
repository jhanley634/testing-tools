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

from time import time
import itertools
import unittest


def permutations(vals):
    '''Pass in a list. All permutations of the list will be generated.'''
    # Itertools is roughly 10x faster.
    # This is the four-step algorithm described (in English) in
    # http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order

    def largest_k(a):
        for k in range(len(a) - 2, -1, -1):
            if a[k] < a[k + 1]:
                return k
        return -1

    def largest_m(k, a):
        for m in range(len(a) - 1, k, -1):
            if a[k] < a[m]:
                return m
        assert None, (k, m, a)  # Can't happen.

    if len(vals) > 0:
        yield tuple(vals)
    k = largest_k(vals)
    while k > -1:
        m = largest_m(k, vals)
        vals[k], vals[m] = vals[m], vals[k]  # Swap k, l.
        vals = vals[:k + 1] + list(reversed(vals[k + 1:]))
        yield tuple(vals)
        k = largest_k(vals)


def powerset_recursive(n):
    if n == 0:
        return []
    return powerset(n - 1) + list(itertools.permutations(tuple(range(n))))


def powerset(n):
    ret = []
    for i in range(n):
        ret.extend(itertools.permutations(tuple(range(i + 1))))
    return ret


class GenTest(unittest.TestCase):

    def assertGenEqual(self, expected_list1, gen2):
        self.assertEqual(expected_list1, list(gen2))


class PowersetTest(GenTest):

    def test_permutations(self):
        self.assertGenEqual([], permutations(list(range(0))))
        self.assertGenEqual([(0,)], permutations(list(range(1))))
        self.assertGenEqual([(0, 1), (1, 0)], permutations(list(range(2))))
        self.assertGenEqual([(0, 1, 2), (0, 2, 1),
                             (1, 0, 2), (1, 2, 0),
                             (2, 0, 1), (2, 1, 0),
                             ], permutations(list(range(3))))
        self.assertGenEqual([(0, 1, 2, 3), (0, 1, 3, 2),
                             (0, 2, 1, 3), (0, 2, 3, 1),
                             (0, 3, 1, 2), (0, 3, 2, 1),
                             (1, 0, 2, 3), (1, 0, 3, 2),
                             (1, 2, 0, 3), (1, 2, 3, 0),
                             (1, 3, 0, 2), (1, 3, 2, 0),
                             (2, 0, 1, 3), (2, 0, 3, 1),
                             (2, 1, 0, 3), (2, 1, 3, 0),
                             (2, 3, 0, 1), (2, 3, 1, 0),
                             (3, 0, 1, 2), (3, 0, 2, 1),
                             (3, 1, 0, 2), (3, 1, 2, 0),
                             (3, 2, 0, 1), (3, 2, 1, 0),
                             ], permutations(list(range(4))))

    def test_pset_correctness(self):
        self.assertEqual([], powerset(0))
        self.assertEqual([(0,)], powerset(1))
        self.assertEqual([(0,), (0, 1), (1, 0)], powerset(2))
        self.assertEqual([(0,), (0, 1), (1, 0),
                          (0, 1, 2), (0, 2, 1),
                          (1, 0, 2), (1, 2, 0),
                          (2, 0, 1), (2, 1, 0)], powerset(3))
        self.assertEqual(9, len(powerset(3)))

    def test_timing(self, n=10):
        '''Evaluating at n=11 would give 43,954,713 elements in 26 sec.'''
        for pset in [powerset, powerset_recursive]:  # 1.15s vs 1.31s
            t0 = time()
            self.assertEqual(4037913, len(pset(n)))
            self.assertLess(time() - t0, 1.8)


if __name__ == '__main__':
    unittest.main()

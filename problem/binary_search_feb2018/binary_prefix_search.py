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

"""Finds a (prefix) needle in a haystack, with binary search.

Suitable for rapidly locating a user input search term in a corpus,
as the user may type just a short prefix.
"""
import collections
import random
import unittest


class OrderedSet:
    """Feeding pre-sorted input data to an OrderedSet may reduce sort() work.
    """

    def __init__(self, iterable):
        self.d = collections.OrderedDict()
        for item in iterable:
            self.d[item] = 1

    def __iter__(self):
        return iter(self.d.keys())


def _verify_strictly_increasing(haystack):
    """Haystack items shall be strictly increasing - no dups."""
    for i in range(len(haystack) - 1):
        assert haystack[i] < haystack[i + 1], (i, haystack[i])


def _verify_monotonic(haystack):
    """Haystack items shall be non-descending. Dups are OK."""
    prev = haystack[0]
    for item in haystack:
        assert item >= prev, item
        prev = item


def _find_match_linear(needle, sorted_haystack):  # Slow, but correct.
    # If haystack contains dups, only 1st occurrence will be accessible.
    _verify_monotonic(sorted_haystack)
    for i, entry in enumerate(sorted_haystack):
        if entry >= needle:
            if (len(entry) >= len(needle)
                    and entry[:len(needle)] == needle):
                return i
            else:
                return None
    return None


def find_match(needle, sorted_haystack, lo=0, hi=None):
    """Returns haystack index of matching entry, or None.

    A haystack entry matches if it is identical to needle,
    or if it is the smallest (first) entry for which needle is a prefix.
    """
    haystack = sorted_haystack
    _verify_strictly_increasing(haystack)

    i = find_exact_match(needle, haystack)
    assert 0 <= i < len(haystack), i
    entry = haystack[i]
    if (len(entry) >= len(needle)
            and entry[:len(needle)] == needle):
        return i
    return None


def find_exact_match(needle, sorted_haystack, lo=0, hi=None):
    """Returns haystack index of matching entry, or index before hole.
    """
    haystack = sorted_haystack
    if hi is None:
        hi = len(haystack)
    assert len(haystack) > 0
    if hi - lo == 1:
        return lo

    while hi - lo >= 2:
        mid = int((lo + hi) / 2)
        if haystack[mid] == needle:
            return mid
        if haystack[mid] < needle:
            lo = mid
        else:
            hi = mid

    assert hi - lo == 1, (hi, lo, needle)
    return lo


class BinarySearchTest(unittest.TestCase):

    def setUp(self):
        self.haystack = sorted(OrderedSet(self.get_chaff()))

    def get_chaff(self, max_length=6, infile='/usr/share/dict/words'):
        # get_hay(?)
        """Generates English lowercase words of at most max_length."""
        with open(infile) as fin:
            for line in fin:
                word = line.rstrip()
                if len(word) <= max_length:
                    yield word.lower()

    def test_dups_ok(self):
        hstack = 'ape bat cat cat cat dog'.split()
        self.assertEqual(0, _find_match_linear('', hstack))
        self.assertEqual(0, _find_match_linear('a', hstack))
        self.assertIsNone(_find_match_linear('aardvark', hstack))
        self.assertEqual(2, _find_match_linear('cat', hstack))
        self.assertEqual(5, _find_match_linear('dog', hstack))
        self.assertIsNone(_find_match_linear('elephant', hstack))

    def test_dups_not_allowed(self):
        hstack = 'ape bat cat cat cat dog'.split()
        with self.assertRaises(AssertionError):
            find_match('bat', hstack)

    def test_linear_search(self):
        self.assertEqual(640, BinarySearchTest.maxDiff)
        # BinarySearchTest.maxDiff = None
        # unittest.util._MAX_LENGTH = 601000

        # seen = set()
        # for word in self.haystack:
        #     if word[:-1] in seen:
        #         print(word)
        #     seen.add(word)

        self.assertGreaterEqual(len(self.haystack), 33000)

        self.assertNotIn('yuc', self.haystack)
        self.assertIn('yuck', self.haystack)
        self.assertIn('yucky', self.haystack)
        self.assertNotIn('yuckz', self.haystack)

        i = _find_match_linear('yuc', self.haystack)
        self.assertEqual(33625, i)
        self.assertEqual('yuca', self.haystack[i])

        i = _find_match_linear('yuck', self.haystack)
        self.assertEqual(33628, i)
        self.assertEqual('yuck', self.haystack[i])

        self.assertIsNone(_find_match_linear('yuckz', self.haystack))

    def test_binary_exact_search(self):

        self.assertEqual(0, find_exact_match('', self.haystack))
        self.assertEqual(0, find_exact_match('7', self.haystack))
        self.assertEqual('a', self.haystack[0])

        i = find_exact_match('conf', self.haystack)
        self.assertEqual('cone coned coneen coner cones confab',
                         ' '.join(self.haystack[i - 4 : i + 2]))
        self.assertEqual(6521, i)

        i = find_exact_match('yuc', self.haystack)
        self.assertEqual('yuca', self.haystack[i + 1])
        self.assertEqual(33624, i)

        i = find_exact_match('yuck', self.haystack)
        self.assertEqual('yuck', self.haystack[i])
        self.assertEqual(33628, i)

        i = find_exact_match('yuckz', self.haystack)
        self.assertEqual('yucky', self.haystack[i])
        self.assertEqual('yuechi', self.haystack[i + 1])
        self.assertEqual(33632, i)

        i = find_exact_match('~', self.haystack)
        self.assertEqual('zythum', self.haystack[i])
        self.assertEqual(len(self.haystack) - 1, i)

    def test_binary_search(self):
        self.assertIsNone(find_match('yuc', self.haystack))

        i = find_match('yuck', self.haystack)
        self.assertEqual('yuck', self.haystack[i])
        self.assertEqual(33628, i)

        self.assertIsNone(find_match('yuckz', self.haystack))

    def test_many_binary_search_terms(self):
        random.seed(42)
        for _ in range(100):
            i = random.randrange(len(self.haystack))
            needle = self.haystack[i].lower()
            self.assertEqual(i, find_match(needle, self.haystack))
            self.assertIsNone(find_match(needle + 'xyzzy', self.haystack))

            while len(needle) > 0:
                j = find_exact_match(needle, self.haystack)
                self.assertLessEqual(j, i)
                i = j
                needle = needle[:-1]


if __name__ == '__main__':
    unittest.main()

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

from problem.longest_prefix.longest_prefix import (longest_prefixes,
                                                   longest_prefix_match as match)


class LongestPrefixTest(unittest.TestCase):

    def test_match(self):
        self.assertEqual(0, match('', ''))
        self.assertEqual(0, match('a', ''))
        self.assertEqual(0, match('', 'b'))
        self.assertEqual(0, match('a', 'b'))
        self.assertEqual(1, match('a', 'a'))
        self.assertEqual(1, match('aa', 'ab'))
        self.assertEqual(1, match('ab', 'aa'))
        self.assertEqual(2, match('abc', 'abd'))
        self.assertEqual(3, match('abc', 'abc'))
        self.assertEqual(3, match('abc', 'abcd'))

    @staticmethod
    def get_lines(words, fspec='/tmp/words.txt'):
        with open(fspec, 'w') as fout:
            fout.write((words + ' ').replace(' ', '\n'))
        return fspec

    @classmethod
    def prefixes(cls, words):
        return list(longest_prefixes(cls.get_lines(words)))

    def test_longest_prefixes(self):
        self.assertEqual(['a', 'c'], self.prefixes('a c cc cd'))
        self.assertEqual(['a', 'c'], self.prefixes('\na c cc cd'))
        self.assertEqual(['a', 'c'], self.prefixes('a aa aa ab c cc cd'))

        self.assertEqual(['bar-12', 'bar-1', 'bazz-'],
                         self.prefixes('bar-12 bar-13 bar-14 bazz-51 bazz-61'))

        self.assertEqual(['bar-12', 'bar-', 'bazz-'],
                         self.prefixes('bar-12 bar-34 bar-5 bazz-51 bazz-61'))

        self.assertEqual(['bar-12', 'bar-', 'bazz-', 'clk'], self.prefixes(
            'bar-12 bar-34 bar-5 bazz-51 bazz-61 bazz-62 clk1 clk2'))

        self.assertEqual(['bazz-51', 'bazz-6', 'clk'],
                         self.prefixes('bazz-51 bazz-61 bazz-62 clk1 clk2'))

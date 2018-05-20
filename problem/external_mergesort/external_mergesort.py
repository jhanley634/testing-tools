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

import itertools
import random
import unittest

from bs4 import BeautifulSoup
import requests


def merge_streams(a, b):
    """Given pre-sorted iterables A and B, yields their sorted union.
    """
    a_item, valid = _get_next(a)
    if not valid:  # Input A was empty.
        yield from b
        return

    b_item, valid = _get_next(a)
    if not valid:  # Input B was empty.
        yield a_item
        yield from a
        return

    # Loop invariant:
    #   We have a & b items we can compare, and
    #   both streams still potentially have items to consume.

    while True:

        if a_item <= b_item:
            yield a_item
            a_item, valid = _get_next(a)
            if not valid:  # We found the end of A.
                yield b_item
                yield from b
                return

        else:

            yield b_item
            b_item, valid = _get_next(b)
            if not valid:  # We found the end of B.
                yield a_item
                yield from a
                return


def _get_next(it):
    try:
        return next(it), True
    except StopIteration as e:
        return None, False


# From https://docs.python.org/3/library/itertools.html#itertools-recipes
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


class ItemCountGenerator:
    """Produces an order sequence of (item, count) tuples, as a testing aid.
    """

    def __init__(self, num_valid_items=3, seed=None):
        k = num_valid_items
        assert k <= 20
        self.valid_items = take(k, self._get_nato_letters())
        # self.valid_items = take(k, self._get_valid_items())
        if seed:
            random.seed(seed)

    def generate(self):
        while True:
            i = random.randrange(len(self.valid_items))
            yield self.valid_items[i]

    @staticmethod
    def _vowel_count(s):
        return sum(map(s.count, 'aeiouy'))

    def _get_valid_items(self, words='/usr/share/dict/web2a', size=4):
        next = '`'  # next candidate prefix
        with open(words) as fin:
            for line in fin:
                if line <= next:
                    continue
                word = line.split()[0].lower()
                if (len(word) == size
                        and self._vowel_count(word) == 1):
                    yield word
                    next = chr(1 + ord(word[0]))

    def _get_nato_letters(self):
        url = 'https://en.wiktionary.org/wiki/Appendix:NATO_phonetic_alphabet'
        r = requests.get(url)
        tbl = BeautifulSoup(r.text, 'html5lib').find('table')
        for row in tbl.find_all('tr'):
            tds = list(row.find_all('td'))
            if tds and len(tds[0].text) == 1:
                letter_text = tds[1].text.lower()
                yield letter_text.split()[-1]  # This handles xray.


class ExternalMergesortTest(unittest.TestCase):

    def test_one_empty(self):
        a = iter('')
        b = iter('xy')
        self.assertEqual('xy', ''.join(merge_streams(a, b)))

        a = iter('xy')
        b = iter('')
        self.assertEqual('xy', ''.join(merge_streams(a, b)))

    def test_interleaved(self):
        a = iter('abxyz')
        b = iter('cdef')
        self.assertEqual('abcdefxyz', ''.join(merge_streams(a, b)))

        a = iter('abddexyz')
        b = iter('ceeff')
        self.assertEqual('abcddeeeffxyz', ''.join(merge_streams(a, b)))


if __name__ == '__main__':
    ic_gen = ItemCountGenerator(seed=42)
    k = 3
    a = iter(take(2 * k, ic_gen.generate()))
    b = iter(take(k, ic_gen.generate()))

    lst = list(merge_streams(a, b))

    unittest.main()

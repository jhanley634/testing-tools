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


_sentinel = object()


def merge_streams(a, b):
    """Given pre-sorted iterables A and B, yields their sorted union.
    """
    stream = (a, b)
    item = list(map(_get_next, stream))
    cur_stream = _get_cur_stream_idx(item)  # Stream we are reading ATM.

    while item != [_sentinel, _sentinel]:  # While at least one not at EOF.
        yield item[cur_stream]
        item[cur_stream] = _get_next(stream[cur_stream])
        cur_stream = _get_cur_stream_idx(item)


def _get_cur_stream_idx(item):
    for i in range(2):
        if item[i] == _sentinel:
            return 1 - i  # The non-sentinel value wins.

    return min(enumerate(item), key=lambda x: x[1])[0]  # argmin


def _get_next(it):
    try:
        return next(it)
    except StopIteration:
        return _sentinel


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

    def test_both_empty(self):
        a = iter('')
        b = iter('')
        self.assertEqual('', ''.join(merge_streams(a, b)))

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

    def test_generated_items(self):
        ic_gen = ItemCountGenerator(seed=42)
        k = 100
        a = iter(take(2 * k, ic_gen.generate()))
        b = iter(take(k, ic_gen.generate()))

        self.assertEqual(3 * k, len(list(merge_streams(a, b))))


if __name__ == '__main__':
    unittest.main()

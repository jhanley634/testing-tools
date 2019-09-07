#! /usr/bin/env python3

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


def _get_chars_plus_sentinel(s):
    yield from s
    yield None  # sentinel


def compress_rle(s: str):
    """Compresses letters, e.g. AAA -> A3, leaving A alone (since A1 would be longer)."""
    # This is a primitive Run Length Encoding scheme.
    # Since digits are prohibited in the input, a compressed output token
    # like A24 is unambiguous, we know '4' was not in the input.
    ret = []
    prev = None
    count = 0
    for c in _get_chars_plus_sentinel(s):
        assert str(c).isalpha(), f'input must be alphabetic letters, but it contained {c}'
        if c != prev:
            if prev:
                ret.append(prev)
                if count > 1:
                    ret.append(str(count))
            count = 0
            prev = c
        count += 1

    return ''.join(ret)


def _get_tokens(s):
    count = 0
    ch = None
    for c in _get_chars_plus_sentinel(s):
        if str(c).isdigit():  # The text 'None" is not a digit.
            count *= 10
            count += int(c)
        else:
            if ch:
                yield ch, count if count else 1
            ch = c
            count = 0


def uncompress_rle(compressed: str):
    """Run length decoder, turns e.g. A3 into AAA"""
    return ''.join(ch * count
                   for ch, count in _get_tokens(compressed))


class Compress(unittest.TestCase):

    def test_compress_run_length_encoder(self):
        msg = 'xyyyyzz'
        for i in range(9, 13):
            msg += 'j' + 'k' * i

        self.assertEqual('xy4z2jk9jk10jk11jk12', compress_rle(msg))

        while msg:
            self.assertEqual(msg, uncompress_rle(compress_rle(msg)))
            msg = msg[1:]

        self.assertEqual('', uncompress_rle(compress_rle('')))

    def test_compress_validates_the_input_message(self):
        msg = 'A24'  # Digits may not appear in the input message -- this is enforced.
        with self.assertRaises(AssertionError):
            compress_rle(msg)

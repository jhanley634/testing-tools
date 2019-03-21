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

import sys
import uuid

import pandas as pd


class ListAllocator:

    # 25 bytes for things like length, according to sys.getsizeof()
    _OVERHEAD = 25

    _UUID_LEN = 36

    N = int(1e5)

    BIG = 'x' * (N - _OVERHEAD - _UUID_LEN)

    @classmethod
    def get_big_string(cls):
        # We intern a different str object on each iteration.
        return str(uuid.uuid4()) + cls.BIG

    def __init__(self):
        self.big_list = []

    def allocate(self, bytes):
        n = 0
        lst = []
        while n < bytes:
            big = self.get_big_string()
            lst.append(big)
            n += sys.getsizeof(big)
        self.big_list = lst
        return n


class DictAllocator(ListAllocator):

    def __init__(self):
        self.big_dict = {}

    def allocate(self, bytes):
        n = 0
        d = {}
        while n < bytes:
            big = self.get_big_string()
            d[len(d)] = big
            n += sys.getsizeof(big)
        self.big_dict = d
        return n


class DfAllocator(ListAllocator):

    def allocate(self, bytes):
        n = 0
        lst = []
        while n < bytes:
            big = self.get_big_string()
            df = pd.DataFrame([dict(id=1, val=big)])
            lst.append(df)
            n += sys.getsizeof(big)
        self.big_list = lst
        return n

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


class ListAllocator:

    # 25 bytes for things like length, according to sys.getsizeof()
    _OVERHEAD = 25

    BIG = 'x' * int(1e5 - _OVERHEAD)

    @classmethod
    def allocate(cls, bytes):
        n = 0
        lst = []
        while n < bytes:
            lst.append(cls.BIG)
            n += sys.getsizeof(cls.BIG)
        return n

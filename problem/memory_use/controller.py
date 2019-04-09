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

"""Repeatedly invokes memory hog to measure usage."""

import gc
import math
import os
import pprint
import subprocess

from memory_use.allocator import ListAllocator


def find_acceptable_memory_size(type_):
    meg = 2 ** 20
    successful_size = size = bottom = meg  # initial target allocation is one megabyte
    top = math.inf  # top is always greater than acceptable size, will cause failure
    accuracy_threshold = 10 * meg
    while top - bottom > accuracy_threshold:
        cmd = 'memory_use/mem_hog.py --bytes={}'.format(size)
        p = subprocess.run(cmd, shell=True)
        if p.returncode:
            assert 137 == p.returncode, p.returncode  # malloc fail
            top = size
        else:
            bottom = successful_size = size  # Yay! We survived.

        if top == math.inf:
            size *= 2  # The sky's the limit! (so far)
        else:
            size = (top - bottom) // 2 + bottom  # binary search

    return successful_size


def _helper(size):
    a = ListAllocator()
    return a.allocate(size)


def allocate_then_out_of_scope(size, k=12):
    for _ in range(k):
        print(size, _)
        assert _helper(size) >= size


def allocate_then_del(size, k=12):
    a = ListAllocator()
    for _ in range(k):
        print(size, _)
        assert a.allocate(size) >= size
        del a.big_list


def show():
    """Shows GC stats, to help identify when garbage collection was invoked."""
    print('GC counts:', gc.get_count())
    pprint.pprint(gc.get_stats())


def main(type_='list', margin=.10):
    show()
    size = int((1 - margin) * find_acceptable_memory_size(type_))  # 90% of max mem size
    show()
    allocate_then_out_of_scope(size)
    show()
    allocate_then_del(size)
    show()
    # allocate_then_del(int(1.4 * size))  # This, predictably, will fail.


if __name__ == '__main__':
    os.chdir('../problem')
    main()

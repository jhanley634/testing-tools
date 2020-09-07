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

'''
This explores the cost of copying (X, Y) values into X & Y arrays
in order to gain the speed benefit of the builtin min() function.
It turns out that lambdas, for the key function, are expensive.
Ubuntu xenial timings were on an Intel Core i3-3220 CPU @ 3.30GHz.
'''

import contextlib
import random
import sys
import time


class Timer(contextlib.ContextDecorator):
    def __enter__(self):
        self._cpu0 = time.process_time()
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self._t0
        self.cpu_sec = time.process_time() - self._cpu0

    def __str__(self):
        return '%.3f CPU sec in %.3f sec' % (self.cpu_sec, self.elapsed)


def scan_manually_with_if(points):
    x_min = y_min = sys.maxsize
    x_max = y_max = -sys.maxsize
    for p in points:
        if x_min > p[0]:
            x_min = p[0]
        if x_max < p[0]:
            x_max = p[0]
        if y_min > p[1]:
            y_min = p[1]
        if y_max < p[1]:
            y_max = p[1]
    return x_min, x_max, y_min, y_max


def scan_with_two_copies(points):
    xs = [p[0] for p in points]
    x_min = min(xs)
    x_max = max(xs)
    ys = [p[1] for p in points]
    y_min = min(ys)
    y_max = max(ys)
    return x_min, x_max, y_min, y_max


def assign_box(points):
    # from https://codereview.stackexchange.com/questions/155893/find-nearest
    x_min = min(p[0] for p in points)
    x_max = max([p[0] for p in points])
    y_min = min(p[1] for p in points)
    y_max = max(p[1] for p in points)
    return x_min, x_max, y_min, y_max


def scan_with_key(points):
    x_min = min(points, key=lambda p: p[0])[0]
    x_max = max(points, key=lambda p: p[0])[0]
    y_min = min(points, key=lambda p: p[1])[1]
    y_max = max(points, key=lambda p: p[1])[1]
    return x_min, x_max, y_min, y_max


def scan_manually_with_min_max(points):
    x_min = y_min = sys.maxsize
    x_max = y_max = -sys.maxsize
    for p in points:
        x_min = min(p[0], x_min)
        x_max = max(p[0], x_max)
        y_min = min(p[1], y_min)
        y_max = max(p[1], y_max)
    return x_min, x_max, y_min, y_max


def bench(fudge=0):
    points = get_points()

    for time_limit, fn in [
            (.020, scan_manually_with_if),
            (.021, scan_with_two_copies),
            (.030, assign_box),
            (.052, scan_with_key),
            (.086, scan_manually_with_min_max),
            ]:
        with Timer() as t:
            x_min, x_max, y_min, y_max = fn(points)
        assert t.elapsed <= time_limit + fudge, t.elapsed
        print('%.3fs ' % t.elapsed, fn.__name__)
        check(x_min, x_max, y_min, y_max)


def check(x_min, x_max, y_min, y_max, verbose=False):
    '''Verify we obtained the correct answer.'''
    if verbose:
        print(x_min, x_max, y_min, y_max, '\n')
    assert -999987 == x_min, x_min
    assert 999972 == x_max, x_max
    assert -999987 == y_min, y_min
    assert 999988 == y_max, y_max


def get_points(n=1e5, big=1e6):
    random.seed(42)
    return [(random.randint(-big, big),
             random.randint(-big, big))
            for _ in range(int(n))]


if __name__ == '__main__':
    bench()

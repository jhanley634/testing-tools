
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

from math import exp, log


def _relative_error(a, b):
    return (a - b) / b


def sqrt_logarithm(n):
    return exp(log(n) / 2)


def sqrt_newton_raphson(n, rel_error=1e-6):
    n = n or rel_error
    assert n > 0

    root = 1
    while abs(_relative_error(root * root, n)) > rel_error:
        root = (root + n / root) / 2
    return root


def sqrt_binary_search(n, rel_error=1e-6):
    n = n or rel_error
    assert n > 0

    lower, upper = 1, n
    if n < 1:
        lower, upper = n, 1  # answer shall be larger than N in this case

    root = 1
    while abs(_relative_error(root * root, n)) > rel_error:
        root = (lower + upper) / 2
        if root * root < n:
            lower = root
        else:
            upper = root
    return root

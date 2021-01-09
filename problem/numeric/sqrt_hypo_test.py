#! /usr/bin/env python

# Copyright 2021 John Hanley.
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

from hypothesis import given
import hypothesis.strategies as st

from problem.numeric.sqrt import _relative_error
from problem.numeric.sqrt import sqrt_binary_search as bin_sqrt
from problem.numeric.sqrt import sqrt_newton_raphson as nr_sqrt

ϵ = 1e-12
big_float = 1.797e308


@given(st.floats(min_value=ϵ ** 26, max_value=big_float))
def hypo_test_sqrt_rel_error_binary(n: float):
    r = bin_sqrt(n, rel_error=ϵ)
    assert abs(_relative_error(r * r, n)) < ϵ


@given(st.floats(min_value=ϵ ** 26, max_value=big_float))
def hypo_test_sqrt_rel_error_newton_raphson(n: float):
    r = nr_sqrt(n, rel_error=ϵ)
    assert abs(_relative_error(r * r, n)) < ϵ


if __name__ == '__main__':
    assert ϵ ** 26 == 1e-312
    hypo_test_sqrt_rel_error_binary()
    hypo_test_sqrt_rel_error_newton_raphson()

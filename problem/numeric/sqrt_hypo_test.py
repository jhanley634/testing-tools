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
import problem.numeric.sqrt as approx

# Recall that a 64-bit float has this layout:
#    1 bit:   sign
#   11 bits:  exponent
#   52 bits:  a 53-bit mantissa, with implicit leading '1' bit
# https://en.wikipedia.org/wiki/Double-precision_floating-point_format
# The exponent is in biased form: a stored value of 1023 represents zero.
# Exponents of −1023 (all 0s) and +1024 (all 1s) are reserved for special numbers.
# Exponents range from −1022 to +1023.
# We additionally fill in some 1s in the mantissa.
big_float = 2 ** 1023.99999999999994315658113

ϵ = 1e-12


@given(st.floats(min_value=ϵ ** 26, max_value=big_float))
def hypo_test_sqrt_log(n: float):
    r = approx.sqrt_logarithm(n)
    assert abs(_relative_error(r * r, n)) < ϵ


@given(st.floats(min_value=ϵ ** 26, max_value=big_float))
def hypo_test_sqrt_binary(n: float):
    r = approx.sqrt_binary_search(n, rel_error=ϵ)
    assert abs(_relative_error(r * r, n)) < ϵ


@given(st.floats(min_value=ϵ ** 26, max_value=big_float))
def hypo_test_sqrt_newton_raphson(n: float):
    r = approx.sqrt_newton_raphson(n, rel_error=ϵ)
    assert abs(_relative_error(r * r, n)) < ϵ


if __name__ == '__main__':

    # Corresponding value for 32-bit float
    # would be 3.40282346639e+38, stored as 0x7f7fffff.
    assert big_float == 1.7976931348621742e+308

    assert ϵ ** 26 == 1e-312

    hypo_test_sqrt_log()
    hypo_test_sqrt_binary()
    hypo_test_sqrt_log()

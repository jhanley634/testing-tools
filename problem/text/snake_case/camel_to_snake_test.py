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

import re

from hypothesis import given
import hypothesis.strategies as st

from problem.text.snake_case.camel_to_snake import (camel_to_snake,
                                                    snake_to_camel)

armenian_small_ligature = '\u0587'  # .upper() gives a pair of independent letters(!)


def _is_sensible_char(c: str) -> bool:
    """Returns False for certain oddly accented characters, such as İ."""
    assert len(c) == 1
    return c.upper().lower() == c.lower()  # Will it roundtrip, as US-ASCII chars do?


# https://docs.python.org/3/library/re.html
# \Z: Matches only at the end of the string. (unlike $, which also matches newline)
make_snake_re = re.compile(r'^[a-z]+(_[a-z][\w]+)*\Z')  # matches method names for python

# e.g. a_0 --> a0
underscore_digit_re = re.compile(r'_(\d)')


@given(st.from_regex(make_snake_re))
def hypo_test_camel_snake_roundtrip(snake: str):

    snake = ''.join(filter(_is_sensible_char, snake)).rstrip('_').lower()

    snake = underscore_digit_re.sub(r'\1', snake)

    u = snake.upper()
    print(len(snake), snake, u)
    assert snake.lower().upper() == u
    assert u.lower().upper() == u

    snake = snake[0] + snake[1:]
    snake = snake.replace('__', '_')
    camel = snake_to_camel(snake)
    assert camel_to_snake(camel) == snake, (snake, camel, camel_to_snake(camel))


if __name__ == '__main__':
    hypo_test_camel_snake_roundtrip()

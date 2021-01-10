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

make_snake_re = re.compile(r'^[a-z]+(_[a-z]+)*$')  # matches method names for python


@given(st.from_regex(make_snake_re))
def hypo_test_camel_snake_roundtrip(snake: str):

    camel = snake_to_camel(snake)
    assert camel_to_snake(camel) == snake


if __name__ == '__main__':
    hypo_test_camel_snake_roundtrip()

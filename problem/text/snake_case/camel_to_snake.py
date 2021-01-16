
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


def snake_to_camel(s: str) -> str:
    """foo_bar --> fooBar.

    Case of initial letter, in input & output, shall match.
    """
    assert s > '', s
    assert '__' not in s, s
    assert s == s.strip('_')
    words = list(map(str.title, s.split('_')))
    if s[0].islower():
        words[0] = words[0].lower()
    return ''.join(words)


def camel_to_snake(s: str) -> str:
    """fooBar --> foo_bar.

    Case of initial letter, in input & output, shall match.
    """
    assert s > '', s
    snake = s[0]

    for c in s[1:]:
        is_digit = (not c.islower()) and (not c.isupper())
        if c.isupper() and not is_digit:
            snake += '_'
        snake += c.lower()

    return snake

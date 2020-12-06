#! /usr/bin/env python

# Copyright 2020 John Hanley.
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

def _display_unicode_row(ch: str, n=4):
    line = f'{ch}   ' * n
    print(f"{line}\n  {line}\n{line}\n")


hex_horiz = '\u2394'
hex_pointy = '\u2b21'
black_horiz = '\u2b23'
black_pointy = '\u2b22'
x_super = '\u2093'


def display_unicode_example():
    for hex in [hex_horiz, hex_pointy,
                black_horiz, black_pointy]:
        _display_unicode_row(hex)


def _sub(s: str, hx=hex_horiz):
    s = s.replace('a', '\u2597')  # Quadrant lower right
    s = s.replace('b', '\u2596')  # Quadrant lower left
    return s.replace('x', hx)


def display_ascii_horiz_height2_example(n=3, reps=4):
    line1 = r'/ab\__' * n
    line2 = r'\__/ab' * n
    for i in range(reps):
        print('\n'.join(map(_sub, (line1, line2))))


def display_ascii_horiz_height3_example(n=3, reps=4, hex=hex_horiz):
    line1 = (r' /   \  y ' * n).replace('y', x_super)
    line2 = r'(  x  )---' * n
    line3 = r' \___/  . ' * n
    for i in range(reps):
        print('\n'.join((line1, line2, line3)))


if __name__ == '__main__':
    display_unicode_example()
    display_ascii_horiz_height2_example()
    display_ascii_horiz_height3_example()

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

from binascii import unhexlify
from functools import lru_cache
from operator import itemgetter
import json

import colormath.color_conversions as cv
import colormath.color_diff as cd
import colormath.color_objects as co
import seaborn as sns

assert 949 == len(sns.xkcd_rgb)  # e.g. 'very light green': '#d1ffbd'


def _hex_to_rgb(hx: str) -> tuple:
    hx = hx.lstrip('#')
    assert 6 == len(hx), hx
    r, g, b = unhexlify(hx)
    return r, g, b


@lru_cache()
def get_name_to_srgb() -> dict:
    keys = sns.xkcd_rgb.keys()
    return dict(zip(keys, sns.xkcd_palette(keys)))


def _red_check():
    red = co.BaseRGBColor(*_hex_to_rgb('#ff000d'), is_upscaled=True)
    assert red.is_upscaled
    red = get_name_to_srgb()['bright red']
    red = co.sRGBColor(*red)
    assert not red.is_upscaled
    assert '#ff000d' == red.get_rgb_hex() == sns.xkcd_rgb['bright red']


@lru_cache()
def get_color_by_name(name) -> co.sRGBColor:
    return co.sRGBColor(*get_name_to_srgb()[name])


def distance_between_colors(c1: co.sRGBColor,
                            c2: co.sRGBColor) -> float:
    assert isinstance(c1, co.sRGBColor), 'pass a proper color, please'
    return cd.delta_e_cie2000(cv.convert_color(c1, co.LabColor),
                              cv.convert_color(c2, co.LabColor))


def distance_to_all_colors(c1: co.sRGBColor, thresh_dist=22):
    dist = {name: distance_between_colors(c1, get_color_by_name(name))
            for name in sns.xkcd_rgb.keys()}
    dist = {name: round(distance, 2)
            for name, distance in sorted(dist.items(), key=itemgetter(1))
            if distance < thresh_dist}
    return dist


if __name__ == '__main__':
    _red_check()

    red = get_color_by_name('bright red')
    for name in 'bright red,red,pink,purple,violet,blue'.split(','):
        d = distance_between_colors(red, get_color_by_name(name))
        print(round(d, 1), name)

    d = distance_to_all_colors(red)
    print('')
    print(json.dumps(d, indent=4))

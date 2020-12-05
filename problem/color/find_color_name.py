#! /usr/bin/env python

from functools import lru_cache

import colormath.color_diff as cd
import colormath.color_objects as co
import colormath.color_conversions as cv
import seaborn as sns

assert 949 == len(sns.xkcd_rgb)  # e.g. 'very light green': '#d1ffbd'


@lru_cache()
def get_name_to_srgb():
    keys = sns.xkcd_rgb.keys()
    return dict(zip(keys, sns.xkcd_palette(keys)))


def _red_check():
    red = get_name_to_srgb()['bright red']
    red = co.sRGBColor(*red)
    assert not red.is_upscaled
    assert '#ff000d' == red.get_rgb_hex() == sns.xkcd_rgb['bright red']


@lru_cache()
def get_color_by_name(name):
    return co.sRGBColor(*get_name_to_srgb()[name])


def distance_between_colors(c1: co.sRGBColor,
                            c2: co.sRGBColor):
    c1.rgb_r  # pass in some proper colors, please
    return cd.delta_e_cie2000(cv.convert_color(c1, co.LabColor),
                              cv.convert_color(c2, co.LabColor))


if __name__ == '__main__':
    _red_check()

    red = get_color_by_name('bright red')
    for name in 'bright red,red,pink,purple,violet,blue'.split(','):
        d = distance_between_colors(red, get_color_by_name(name))
        print(round(d, 1), name)

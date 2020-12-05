#! /usr/bin/env python

from functools import lru_cache

import colormath as cm
import colormath.color_objects as co
import seaborn as sns

assert 949 == len(sns.xkcd_rgb)  # e.g. 'very light green': '#d1ffbd'


@lru_cache()
def get_name_to_srgb():
    keys = sns.xkcd_rgb.keys()
    return dict(zip(keys, sns.xkcd_palette(keys)))

def red_check():
    red = get_name_to_srgb()['bright red']
    red = co.sRGBColor(*red)
    assert not red.is_upscaled
    assert '#ff000d' == red.get_rgb_hex() == sns.xkcd_rgb['bright red']


if __name__ == '__main__':
    red_check()

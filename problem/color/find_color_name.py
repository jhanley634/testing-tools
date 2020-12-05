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

if __name__ == '__main__':
    print(sns.xkcd_rgb['bright red'])
    red = get_name_to_srgb()['bright red']
    red = co.sRGBColor(*red)
    print(red, red.is_upscaled)
    print(co.sRGBColor(*red.get_value_tuple()),
          co.sRGBColor(*red.get_value_tuple()).is_upscaled)
    up = co.sRGBColor(*red.get_upscaled_value_tuple())
    print(up, up.is_upscaled)

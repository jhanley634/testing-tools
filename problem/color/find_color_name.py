#! /usr/bin/env python

from functools import lru_cache

import seaborn

assert 949 == len(seaborn.xkcd_rgb)  # e.g. 'very light green': '#d1ffbd'


@lru_cache()
def get_name_to_rgb():
    keys = seaborn.xkcd_rgb.keys()
    return dict(zip(keys, seaborn.xkcd_palette(keys)))

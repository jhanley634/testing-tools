#! /usr/bin/env python3

# Copyright 2019 John Hanley.
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

import sys

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib
matplotlib.use('Agg')  # noqa E402
import matplotlib.pyplot as plt
import uszipcode


def get_populous_cities():
    search = uszipcode.SearchEngine()
    for r in search.by_population(1e5):
        print(r.population,
              r.post_office_city)
        yield r.lat, r.lng


def draw_map():

    def colorize_state(geometry):
        return {'facecolor': (.94, .94, .86),
                'edgecolor': (.55, .55, .55)}

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())
    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',
                                         category='cultural', name=shapename)
    ax.add_geometries(
        shpreader.Reader(states_shp).geometries(),
        ccrs.PlateCarree(),
        styler=colorize_state)
    ax.stock_img()

    xs = []
    ys = []
    for lat, lng in get_populous_cities():
        xs.append(lng)
        ys.append(lat)
    ax.plot(xs, ys, 'ok', transform=ccrs.PlateCarree(), markersize=8)

    plt.savefig('/tmp/states.png')


# from https://stackoverflow.com/questions/8315389/print-fns-as-theyre-called
def tracefunc(frame, event, _, indent=[0]):
    if event == "call":
        indent[0] += 2
        file = frame.f_code.co_filename.split('/')[-1]
        print("-" * indent[0] + "> call function", frame.f_code.co_name, file)
    elif event == "return":
        print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        indent[0] -= 2
    return tracefunc


if __name__ == '__main__':
    sys.setprofile(None)  # (tracefunc)
    draw_map()

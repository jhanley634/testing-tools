#! /usr/bin/env python

# Copyright 2018 John Hanley.
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

import os
import re

import folium
import geocoder


def get_lat_lng(addr):
    g = geocoder.osm(addr)
    return g.lat, g.lng


def parse_addresses(fin):
    addr_price_listnum_re = re.compile(r'^(.*?)\s+(\$[\d,]+)\s+MLS (#\w+)')
    addr, price, listnum = '', '', ''
    for line in fin:
        if line.startswith('https://'):
            url = line
            elts = url.split('/')
            assert elts[2].startswith('www.'), elts
            assert elts[3] == 'idx', elts
            addr = elts[4].replace('-', ' ')
            if addr.startswith('526 2nd st '):
                lat, lng = 36.9647, -122.0238
            else:
                lat, lng = get_lat_lng(addr)
            yield (lat, lng), addr, f'{price}  {listnum}  {url}'
        elif addr_price_listnum_re.search(line):
            addr, price, listnum = addr_price_listnum_re.search(line).groups()


def show_addresses(infile='/tmp/addrs.txt', outfile='~/Desktop/map.html'):
    with open(infile) as fin:
        locs = [(loc, addr) for loc, addr, details in parse_addresses(fin)]
        map_ = folium.Map(location=locs[0][0], tiles='Stamen Terrain', zoom_start=14)
        for loc, addr in locs:
            addr = shorten(addr)
            folium.CircleMarker(
                location=loc,
                radius=6,  # px
                color='purple',
                fill=True,
                fill_opacity=.7,
            ).add_to(map_)
            style = 'font-size: 20pt; color: #00008b;'
            folium.map.Marker(
                location=loc,
                icon=folium.DivIcon(
                    icon_size=(100, 200),
                    icon_anchor=(0, 0),
                    html=f'<div style="{style}">{addr}</div>',
                )
            ).add_to(map_)

        map_.save(os.path.expanduser(outfile))


def shorten(addr):
    addr = re.sub(r' \w+ \w+ \w{2} \d+', '', addr)
    return addr.title().replace('Nd ', 'nd ')


if __name__ == '__main__':
    show_addresses()

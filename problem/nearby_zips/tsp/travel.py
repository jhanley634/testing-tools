#! /usr/bin/env python

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
    addr = re.sub(r' \w+ \w+ ca \d+', '', addr)
    return addr.title().replace('Nd ', 'nd ')


if __name__ == '__main__':
    show_addresses()

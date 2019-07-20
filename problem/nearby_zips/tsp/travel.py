#! /usr/bin/env python

import re

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
            yield lat, lng, addr, f'{price}  {listnum}  {url}'
        elif addr_price_listnum_re.search(line):
            addr, price, listnum = addr_price_listnum_re.search(line).groups()


def show_addresses(infile='/tmp/addrs.txt'):
    with open(infile) as fin:
        for lat, lng, addr, details in parse_addresses(fin):
            print(lat, lng)


if __name__ == '__main__':
    show_addresses()

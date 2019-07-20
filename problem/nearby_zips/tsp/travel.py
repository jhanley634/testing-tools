#! /usr/bin/env python

import re


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
            yield addr, f'{price}  {listnum}  {url}'
        elif addr_price_listnum_re.search(line):
            addr, price, listnum = addr_price_listnum_re.search(line).groups()


def show_addresses(infile='/tmp/addrs.txt'):
    with open(infile) as fin:
        for addr, details in parse_addresses(fin):
            print(addr)


if __name__ == '__main__':
    show_addresses()

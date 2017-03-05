#! /usr/bin/env python3

# Copyright 2017 John Hanley.
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


# Given a document snippet uniquely identified by a regex pattern,
# show the hierarchy of web tags above it.
#
# usage:
#     ./tag_from_pattern.py pattern infile [...]


from bs4 import BeautifulSoup
import argparse
import re


def report(pattern, soup):
    for child in soup.body.find_all(string=re.compile(pattern)):
        print(type(child))
        print(child.name)
        print('')


def arg_parser():
    p = argparse.ArgumentParser(description='Show tag hierarchy.')
    p.add_argument('pattern', help='regex which matches just once in a file')
    p.add_argument('infile', nargs='+', help='HTML file(s)')
    return p


if __name__ == '__main__':
    args = arg_parser().parse_args()
    for infile in args.infile:
        assert re.search(r'\.html?$', infile), infile
        with open(infile) as fin:
            html = fin.read()
            report(args.pattern, BeautifulSoup(html, 'html.parser'))

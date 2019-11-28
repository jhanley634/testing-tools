#! /usr/bin/env python

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

import os

import lxml


def _get_urls(top_dir='.', ext='.html'):
    pfx = os.path.abspath(top_dir) + os.path.sep
    for root, dirs, files in os.walk(top_dir):
        for file in files:
            if file.endswith(ext):
                path = os.path.abspath(os.path.join(root, file))[len(pfx):]
                yield path


def gen_sitemap():
    for url in _get_urls(ext='.txt'):
        print(url)


if __name__ == '__main__':
    gen_sitemap()

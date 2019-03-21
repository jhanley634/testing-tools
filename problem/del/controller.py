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

"""Repeatedly invokes memory hog to measure usage."""

import os
import subprocess


def find_acceptable_memory_size(type_):
    size = 1e6  # target allocation of one megabyte
    cmd = './mem_hog.py --target={}'.format(size)
    subprocess.run(cmd, shell=True, check=True)
    return size


def main(type_='list', margin=.10):
    size = (1 - margin) * find_acceptable_memory_size(type_)  # 90% of max mem size
    print(size)


if __name__ == '__main__':
    os.chdir('../del')
    main()

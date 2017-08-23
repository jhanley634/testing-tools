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

import datetime
import glob
import json
import re


def etl_many(files):
    '''Extract, transform, & load a collection of JSON files.'''
    for file in files:
        assert file.endswith('.json'), file
        with open(file) as fin:
            etl1(json.loads(fin.read()))


def etl1(d, user='2002'):
    '''Parse the input dictionary d.'''
    # print(json.dumps(d, sort_keys=True, indent=4))
    assert(d['userId'] == user)
    d['tripId'] = re.sub('^' + user, '', d['tripId'])
    start, end, id = [int(d[k])
                      for k in 'tripStart tripEnd tripId'.split()]
    assert 0 <= start - id < 80, start - id  # id is assigned within 80 msec

    two_sec = 2 * 1e3
    six_sec = 6 * 1e3
    assert 0 < d['tripPoints'][0]['timeStamp'] - start < six_sec
    if end != 0:
        assert 0 < end - d['tripPoints'][-1]['timeStamp'] < two_sec

    longest_journey = 6 * 3600 * 1000  # six hours
    assert end - start < longest_journey, end - start
    if end < start:
        assert end == 0, end  # Four trips exhibit this corrupted end time.

    parse(d['tripPoints'])


def parse(points):
    stamp = 0
    expected = set('bearing edgeId lat lng'
                   ' rpm speed timeStamp timeZone'.split())
    for point in points:
        assert expected == point.keys()
        assert 0 == point['timeZone']
        assert 0 <= point['rpm'] < 4200
        assert 0 <= point['speed'] < 600
        assert stamp < point['timeStamp']  # Breadcrumb stamps are monotonic.
        stamp = point['timeStamp']


def ms_to_date(msec):
    return datetime.datetime.utcfromtimestamp(msec / 1e3)


if __name__ == '__main__':
    etl_many(glob.glob('/tmp/2002/*.json'))

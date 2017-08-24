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
import sys

import sqlalchemy.ext.declarative
from sqlalchemy import Table

sys.path.append('.')
import dbcred

Base = sqlalchemy.ext.declarative.declarative_base()


def etl_many(files):
    '''Extract, transform, & load a collection of JSON files.'''
    for file in files:
        m = re.search(r'(\d+)\.json$', file)
        assert m, file
        file_no = int(m.group(1))
        with open(file) as fin:
            etl1(file_no, json.loads(fin.read()))


def etl1(file_no, d, user='2002'):
    '''Parse the input dictionary d.'''
    # print(json.dumps(d, sort_keys=True, indent=4))
    assert(d['userId'] == user)
    d['tripId'] = re.sub('^' + user, '', d['tripId'])
    start, end, id = [int(d[k])
                      for k in 'tripStart tripEnd tripId'.split()]
    assert 0 <= start - id < 80, start - id  # id is assigned within 80 msec

    six_sec = 6 * 1e3
    assert 0 < d['tripPoints'][0]['timeStamp'] - start < six_sec
    if end != 0:
        assert 0 < end - d['tripPoints'][-1]['timeStamp'] < six_sec

    longest_journey = 6 * 3600 * 1000  # six hours
    assert end - start < longest_journey, end - start
    if end < start:
        assert end == 0, end  # Four trips exhibit this corrupted end time.

    insert(file_no, d['tripPoints'])


def round10(n, k=10):
    return float(round(n * k)) / k


def iso8601(msec):
    d = datetime.datetime.utcfromtimestamp(msec / 1e3)
    return d.strftime('%Y-%m-%d %H:%M:%S')


def insert(file_no, points):
    stamp = 0
    trip_point = Table('crumb_trip_point',
                       META, autoload=True, autoload_with=ENGINE)
    CONN.execute(trip_point.delete().where('file_no=%d' % file_no))
    print('\n%d' % file_no)
    expected = set('bearing edgeId lat lng'
                   ' rpm speed timeStamp timeZone'.split())
    for point in points:
        assert expected == point.keys()
        assert 0 == point['timeZone']
        assert 0 <= point['rpm'] < 4200
        assert 0 <= point['speed'] < 600
        assert stamp < point['timeStamp']  # Breadcrumb stamps are monotonic.
        stamp = point['timeStamp']

        print('.', end='')
        sys.stdout.flush()
        CONN.execute(trip_point.insert().values(
            file_no=file_no,
            stamp=iso8601(stamp),
            lng=point['lng'],
            lat=point['lat'],
            bearing=round10(point['bearing']),
            edge_id=point['edgeId'],
            rpm=point['rpm'],
            speed=point['speed'],
            ))
    CONN.execute('commit')



def ms_to_date(msec):
    return datetime.datetime.utcfromtimestamp(msec / 1e3)


if __name__ == '__main__':
    CONN, ENGINE, META = dbcred.get_cem('breadcrumb')
    dbcred.SESSION.configure(bind=ENGINE, autoflush=False,
                             expire_on_commit=False)
    etl_many(glob.glob('/tmp/2002/*.json'))

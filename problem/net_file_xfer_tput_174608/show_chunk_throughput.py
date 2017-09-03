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

from bs4 import BeautifulSoup
import datetime
import os
import re
import requests

'''Summarizes data from codereview.stackexchange.com/questions/174608/.'''


def get_cached_pastebin_text(url):
    fspec = os.path.basename(url) + '.html'
    if not os.path.exists(fspec):
        r = requests.get(url)
        assert r.ok
        with open(fspec, 'w') as fout:
            fout.write(r.text)

    soup = BeautifulSoup(open(fspec).read(), 'html.parser')
    raw = str(soup.find(id='paste_code'))
    return raw.split('\n')


def hms(stamp):
    '''12:00:00 -> noon.'''
    h, m, s = (int(n) for n in stamp.split(':'))
    today = datetime.date.today()
    return datetime.datetime(
        year=today.year, month=today.month, day=today.day,
        hour=h, minute=m, second=s)


def get_chunks(url='https://pastebin.com/ehncSeqD'):
    chunk_re = re.compile(r'^(\d{2}:\d{2}:\d{2}) - Chunk (\d+) of (\d+)')
    for line in get_cached_pastebin_text(url):
        m = chunk_re.search(line)
        if m:
            yield (hms(m.group(1)),
                   int(m.group(2)),
                   int(m.group(3)))


def show_tput(chunk_size=2e5):
    sentinel = hms('00:00:00')
    prev = sentinel
    for stamp, i, _ in get_chunks():
        if prev != sentinel:
            delta = stamp - prev
            print('%3d   %s elapsed   %.1f bytes/sec' % (
                i, delta, chunk_size / delta.total_seconds()))
        prev = stamp


if __name__ == '__main__':
    os.chdir('/tmp')
    show_tput()

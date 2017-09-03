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
import collections
import datetime
import matplotlib.pyplot as plt
import os
import pprint
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


def get_progress(chunk_size, url='https://pastebin.com/ehncSeqD'):
    chunk_re = re.compile(
        r'^(\d{2}:\d{2}:\d{2}) - Chunk (\d+) of (\d+)')
    detail_re = re.compile(
        r'^(\d{2}:\d{2}:\d{2}) - Interconnect. (\d+) of (\d+)')
    cur_chunk = -1
    for line in get_cached_pastebin_text(url):

        m = chunk_re.search(line)
        if m:
            assert cur_chunk < int(m.group(2))  # strictly monotonic
            cur_chunk = int(m.group(2))

        m = detail_re.search(line)
        if m:
            assert chunk_size >= int(m.group(3))
            yield(hms(m.group(1)),
                  cur_chunk * chunk_size + int(m.group(2)))


def delete_singletons(d, thresh=2):
    '''Given a dictionary of counts, suppresses counts below some threshold.'''
    return {k: v
            for k, v in d.items()
            if v >= thresh}


def plot_tput(chunk_size=2e5, verbose=False):
    prog = {}  # maps elapsed time to download progress (in bytes)
    size_hist = collections.defaultdict(int)  # histogram, maps pkt size to cnt
    prev_bytes = 0
    start = None
    for stamp, bytes in get_progress(int(chunk_size)):
        if start:
            elapsed = int((stamp - start).total_seconds())
            # With limited resolution (1sec) timestamps, last measurement wins.
            prog[elapsed] = bytes
            size = bytes - prev_bytes
            prev_bytes = bytes
            size_hist[size] += 1
            if verbose:
                print(elapsed, size, bytes)
        else:
            start = stamp

    print('pkt_size: count')
    pprint.pprint(delete_singletons(size_hist))

    x = [p[0] for p in prog.items()]
    y = [p[1] / 1024.0 for p in prog.items()]  # total KBytes downloaded so far
    plt.scatter(x, y)
    plt.show()


if __name__ == '__main__':
    os.chdir('/tmp')
    plot_tput()

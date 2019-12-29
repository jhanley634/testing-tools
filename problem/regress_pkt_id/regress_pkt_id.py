#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

# import matplotlib as plt
# import statsmodels.formula.api as sm

import os
import re
import urllib.request

from bs4 import BeautifulSoup
import scipy.stats


class HpingIdFinder:

    def __init__(self):
        self.text = ''
        self.name_to_ip = {}

    def add(self, text):
        self.text += text

        # e.g. HPING ecomm.dell.com (eth0 143.166.83.166): S set, 40 headers...
        hdr_re = re.compile(r'^HPING ([\w\.-]+) .eth\d ([\d\.]+)')
        for line in text.split('\n'):
            m = hdr_re.search(line)
            if m:
                name, ip = m.group(1), m.group(2)
                self.name_to_ip[name] = ip

    def _get_id_rtts(self, hostname):
        '''Parse out packet_id and round_trip_time.'''
        ip = self.name_to_ip[hostname]
        bytes_from_re = re.compile(
            r'^\d+ bytes from %s:'
            r' flags=SA seq=\d+ ttl=\d+ id=(\d+) rtt=([\d\.]+) ms' % ip)
        for line in self.text.split('\n'):
            m = bytes_from_re.search(line)
            if m:
                yield int(m.group(1)), float(m.group(2))

    def _get_one(self, hostname, idx):
        for vals in self._get_id_rtts(hostname):  # Project 2-tuples...
            yield vals[idx]  # ...down to scalars.

    def get_ids(self, hostname):
        return self._get_one(hostname, 0)

    # def get_rtts(self, hostname):
    #     return self._get_one(hostname, 1)


def download(target, url):
    if os.path.exists(target):
        return  # Use the already-cached copy.

    response = urllib.request.urlopen(url)
    bytes = response.read()
    with open(target, 'wb') as fout:
        fout.write(bytes)


def round10(n):
    '''Round to nearest tenth.'''
    return round(float(n * 10)) / 10


def fit(y):
    '''Fit a linear model to list of observed Y values.'''
    x = list(range(len(y)))
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    assert r_value > 0.98, r_value  # It happens our data is highly correlated.
    return round10(slope), round10(intercept)


def main(doc='insecure_stc.html'):
    # A chapter from "Stealing the Network: How to Own a Continent".
    download(doc, 'http://insecure.org/stc/')
    soup = BeautifulSoup(open(doc).read(), 'lxml')
    id_finder = HpingIdFinder()
    for pre in soup.find_all('pre'):
        if '46 bytes from' in pre.text:
            id_finder.add(pre.text)
    for hostname in sorted(id_finder.name_to_ip.keys()):
        ids = list(id_finder.get_ids(hostname))
        print(hostname, fit(ids))


if __name__ == '__main__':
    os.chdir('/tmp')
    main()

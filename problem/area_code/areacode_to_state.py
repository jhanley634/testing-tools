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

"""Supplies an area code to state mapping."""

from pathlib import Path
from urllib.parse import urlparse
import hashlib
import os
import re

import bs4
import requests


def _hash(s: str, k=6):
    """Returns K nybbles of entropy from the input string.

    >>> _hash("Hi!")
    'e652a1'
    """
    return hashlib.sha3_224(s.encode()).hexdigest()[:k]


def _get_id(s: str):
    """Given a string which may contain random garbage such as punctuation,
    returns the prefix that corresponds to a valid identifier.

    >>> _get_id('search-db?q=foo')
    'search-db'
    >>> _get_id('?q=foo')
    ''
    """
    id_re = re.compile(r'^[\w-]*')
    m = id_re.search(s)
    return m.group(0)


def _get_local_cache_filespec(url, cache_dir):
    # The most challenging input URLs would look like: http://example.com/?guid=blah
    # The default K=6 yields 24 bits of entropy. Taking sqrt() for the Birthday Paradox,
    # that leaves us at 2^12. So if you plan to offer more than a few thousand
    # distinct URLs, adjust K in order to avoid collisions.
    components = urlparse(url)
    host = (components.netloc).replace('.', '-')
    fname = os.path.basename(components.path)
    return Path(cache_dir) / f'{host}-{_hash(url)}-{fname}'


def get_cached_web_page(url, cache_dir='/tmp'):
    """Retrieves text of a web page, possibly via a local FS cache hit."""
    fspec = _get_local_cache_filespec(url, cache_dir)
    if not fspec.exists():
        r = requests.get(url)
        r.raise_for_status()
        with open(fspec, 'w') as fout:
            fout.write(r.text)
    with open(fspec) as fin:
        return fin.read()


def get_areacode_to_state():
    """Returns a NANPA telephone area code to state mapping."""
    url = 'https://www.worldatlas.com/na/us/area-codes.html'
    state_link_re = re.compile(r'/namerica/usstates/(\w{2}|washdc).htm$')
    areacode_link_re = re.compile(r'/na/us/\w{2}/area-code-\d{3}.html$')
    state = 'XX'
    soup = bs4.BeautifulSoup(get_cached_web_page(url), 'html5lib')
    tbl = soup.find_all('table')[0]
    for tr in tbl.find_all('tr'):
        for a in tr.find_all('a'):
            href = a.get('href')
            m = state_link_re.search(href)
            if m:
                state = m.group(1)[-2:]
            if areacode_link_re.search(href):
                assert 3 == len(a.text), a
                assert a.text.isdigit(), a
                yield int(a.text), state


if __name__ == '__main__':
    ac_to_state = dict(get_areacode_to_state())
    assert 241 == len(ac_to_state)
    assert 51 == len(set(ac_to_state.values()))
    assert 'dc' == ac_to_state[202]
    assert 'nj' == ac_to_state[201]

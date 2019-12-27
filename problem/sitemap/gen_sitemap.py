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

import datetime as dt
import io
import os

from lxml import etree


def _iso(sec: float) -> str:
    stamp = dt.datetime.fromtimestamp(sec, dt.timezone.utc)
    return stamp.isoformat()


def _get_urls(top_dir='.', ext='.html'):
    p = 1
    pfx = os.path.abspath(top_dir) + os.path.sep
    for root, dirs, files in os.walk(top_dir):
        for file in files:
            if file.endswith(ext):
                path = os.path.join(root, file)
                sec = int(os.path.getmtime(path))
                path = os.path.abspath(path)[len(pfx):]
                p *= .9999  # Newest entries should be crawled first.
                yield dict(loc=path,
                           lastmod=_iso(sec),
                           priority=round(p, 7))


def _item_func(parent):
    return 'url'
    # yield dicttoxml(d, root=False, custom_root='url',
    #   attr_type=False, item_func=_item_func).decode()


def _get_xml_body():
    for d in _get_urls(ext='.txt'):
        yield '  <url>'
        for k, v in d.items():
            yield f'    <{k}>{v}</{k}>'
        yield '  </url>'
    yield '</urlset>'


def _get_preamble():
    return '''<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

'''


def gen_sitemap():

    # parser = etree.XMLParser(dtd_validation=True, no_network=False, ns_clean=True)
    f = io.StringIO(_get_preamble() + '\n'.join(_get_xml_body()))
    etree.parse(f)  # , parser)
    print(f.getvalue())


if __name__ == '__main__':
    gen_sitemap()

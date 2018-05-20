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

"""Finds demographic statistics based on zipcode.
"""
import io
import os
import unittest
import zipfile

import requests
import sqlalchemy
import sqlalchemy.engine.url
import sqlalchemy.exc
import sqlalchemy.ext.automap
import sqlalchemy.orm.session
import uszipcode

# from places_table import t_places
import place_table


class ZipcodeStats:

    def __init__(self, places_mgr=None):
        if places_mgr is None:
            places_mgr = Places2kMgr()
        self.places_mgr = places_mgr
        self.zse = uszipcode.ZipcodeSearchEngine()

    def get_city_state(self, zipcode):
        r = self.zse.by_zipcode(zipcode)
        return '{} {}'.format(r['City'], r['State'])

    def get_lat_lng(self):
        pass


class Place:
    __table__ = 'place'


class Places2kMgr:
    """Manages a sqlite DB originally drawn from
    http://www.census.gov/tiger/tms/gazetteer/places2k.txt.
    """

    def __init__(self, dir='/tmp',
                 db_file='places.db', in_file='places2k.txt'):
        self.engine = None
        db_file, in_file = [os.path.join(dir, f) for f in [db_file, in_file]]

        os.unlink(db_file)

        db_url = sqlalchemy.engine.url.URL(
            **dict(drivername='sqlite', database=db_file))
        self.engine = sqlalchemy.create_engine(db_url)
        if not os.path.exists(db_file):
            if not os.path.exists(in_file):
                self._download(in_file)
            with open(in_file) as fin:
                self._create_database(db_file, fin)

    def _create_database(self, db_file, fin):
        meta = self._ensure_table_exists()
        meta.reflect()
        # meta.reflect(self.engine, only=['place'])
        base = sqlalchemy.ext.automap.automap_base(metadata=meta)
        base.prepare()
        assert 1 == len(base.metadata.sorted_tables)
        # place = base.metadata.sorted_tables[0]

        # sess = sqlalchemy.orm.session.sessionmaker()()
        # Now populate the table.
        for row in self._get_text_file_fields(fin):
            state, fips, name = row[:3]
            # ins = place.insert()

    def _get_text_file_fields(self, fin):
        # Columns 1-2: United States Postal Service State Abbreviation
        # Columns 3-4: State Federal Information Processing Standard FIPS code
        # Columns 5-9: Place FIPS Code
        for line in fin:
            state = line[:2]
            fips = line[2:9]  # First 2 characters give the state FIPS code.
            name = line[9:73].rstrip()
            pop2k = int(line[73:82])
            homes2k = int(line[82:91])  # ignore land area m^2, water, & sq mi
            assert line[143] == ' ', line[143:]  # northern hemisphere
            lat = float(line[143:153])
            lng = float(line[153:164])
            assert lat > 0
            assert lng < 0 or name.startswith('Attu ')  # western hemisphere
            yield state, fips, name, pop2k, homes2k, lat, lng

    def _ensure_table_exists(self):
        meta = sqlalchemy.MetaData(bind=self.engine)
        query = 'select *  from place  where 1 > 2'  # Sqlite lacks 'False'.
        try:
            self.engine.execute(query).fetchall()
        except sqlalchemy.exc.OperationalError:
            meta.create_all(tables=[place_table.t_places])
            self.engine.execute(query).fetchall()
        return meta

    def _download(self, out_file, zip_url='https://www.cs.rutgers.edu/~pxk'
                                          '/rutgers/hw/places.zip'):
        # Another candidate download location might be
        # https://github.com/petewarden/crunchcrawl/raw/master/places2k.txt
        # but it uses some variant Latin1 encoding for Puerto Rico place names.
        req = requests.get(zip_url)
        assert 200 == req.status_code
        assert 1110384 == int(req.headers['Content-Length'])
        assert 'application/zip' == req.headers['Content-Type']
        content = io.BytesIO(req.content)

        zf = zipfile.ZipFile(content)
        fl = zf.filelist
        assert 'places2k.txt' == fl[0].filename
        assert 4212250 == fl[0].file_size
        assert 1507489281 == fl[0].CRC
        assert (2009, 3, 18, 15, 37, 52) == fl[0].date_time

        with zf.open(fl[0].filename) as places, open(out_file, 'w') as fout:
            fout.write(places.read().decode('latin1'))

        assert 4212304 == os.path.getsize(out_file)  # UTF-8 expands slightly.


class ZipcodeStatsTest(unittest.TestCase):

    def setUp(self):
        self.zc = ZipcodeStats()

    def test_city_state(self):
        self.assertEqual('Beverly Hills CA', self.zc.get_city_state('90210'))

    def test_places(self):
        pass


if __name__ == '__main__':
    unittest.main()

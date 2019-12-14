
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

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus
import datetime as dt
import getpass
import glob
import json
import os
import re

import requests
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlite3


class GeocodeCache:
    def __init__(self, db='~/.geocode_db.sqlite'):
        fspec = Path(db).expanduser().resolve()
        self._create_db_file(fspec)
        self.engine = sa.create_engine(f'sqlite:///{fspec}')
        self._create_table()

    def get_session(self):
        return orm.sessionmaker(bind=self.engine)()

    @lru_cache()
    def get_table(self, name, schema=None):
        meta = sa.MetaData(bind=self.engine)
        return sa.Table(name, meta, autoload=True, schema=schema)

    def _create_db_file(self, fspec):
        """If sqlite database file is missing, then create it."""
        conn = sqlite3.connect(fspec)
        conn.close()

    def _create_table(self):
        ddl = '''
            create table geo_cache (
              addr            text  primary key,
              accuracy        real,
              accuracy_type   text,
              lat             real  not null,
              lng             real  not null,
              formatted_addr  text  not null
            )
          '''
        try:
            self.engine.execute(ddl)
        except sa.exc.OperationalError:
            pass

    @staticmethod
    def _get_pairs(input_txt_file):
        """Reads a file of couplets: query, result, query, result."""
        first_word_re = re.compile(r'^(query|result): +(.*)$')
        query = None
        with open(input_txt_file) as fin:
            for line in fin:
                first, rest = first_word_re.search(line).groups()
                if first == 'query':
                    query = rest
                else:
                    yield query, json.loads(rest)
                    query = None

    def store(self, row, addr):
        gc = self.get_table('geo_cache')
        row['addr'] = addr
        try:
            row['formatted_addr'] = row.pop('formatted_address')
        except AttributeError:
            pass
        self.engine.execute(gc.insert(), row)

    def insert_text_file_lines(self, input_txt_file):
        for addr, d in self._get_pairs(input_txt_file):
            if not self.row_if_present(addr):
                print(d)
                self.store(d, addr)

    def insert_text_files(self, log_dir):
        for fspec in glob.glob(f'{log_dir}/*.txt'):
            self.insert_text_file_lines(fspec)

    def row_if_present(self, addr):
        """If table contains the addr key we return the row, else empty dict."""
        gc = self.get_table('geo_cache')
        q = (self.get_session()
             .query(gc.c.lat,
                    gc.c.lng,
                    gc.c.formatted_addr)
             .filter(gc.c.addr == addr))
        row = {}
        try:
            row = q.one()._asdict()
        except sa.orm.exc.NoResultFound:
            pass
        return row


class GeocodioGeocoder:

    def __init__(self, log_dir_pfx='/tmp/geocodio_log_'):
        self._cache = GeocodeCache()
        self._base_url = 'https://api.geocod.io/v1.4'
        self._key = os.environ['GEOCODIO_API_KEY']
        assert 39 == len(self._key), self._key

        self.log_dir = Path(log_dir_pfx + getpass.getuser())
        os.makedirs(self.log_dir, exist_ok=True)
        today = dt.date.today()
        fspec = self.log_dir / f'{today}.txt'
        self._log_file = open(fspec, 'a')  # Only closed (implicitly) when python exits.

    def _log_write(self, s: str):
        self._log_file.write(s)
        self._log_file.write('\n')
        self._log_file.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log_file.close()

    @staticmethod
    def _normalize(addr):
        addr = addr.lower().replace('#', ' unit ').replace(',', ' ')
        return ' '.join(addr.split())  # Squish repeated blanks.

    def geocode(self, full_address):
        return self.code(full_address)  # synonym

    def code(self, full_address):
        norm_address = self._normalize(full_address)
        result = self._cache.row_if_present(norm_address)
        if result:
            return result
        self._log_write(f'query:  {norm_address}')
        # https://api.geocod.io/v1.4/geocode?q=1109+N+Highland+St%2c+Arlington+VA&api_key=...
        url = (f'{self._base_url}/geocode?api_key={self._key}&q='
               + quote_plus(norm_address))
        resp = requests.get(url)
        resp.raise_for_status()
        js = resp.json()['results'][0]
        loc = js['location']
        js.update(loc)
        result = {key: js[key]
                  for key in 'accuracy accuracy_type lat lng formatted_address'.split()}
        self._log_write('result: ' + json.dumps(result))
        self._cache.store(result, norm_address)
        result = self._cache.row_if_present(norm_address)
        assert result['lat'] >= -90
        return result

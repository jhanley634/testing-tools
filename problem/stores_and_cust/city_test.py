
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

import os
import unittest

import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.sql.functions as fn
import uszipcode


class CityTest(unittest.TestCase):

    @staticmethod
    def get_zip_db_file():
        uszipcode.SearchEngine()  # downloads DB file if necessary
        return os.path.expanduser('~/.uszipcode/simple_db.sqlite')

    def setUp(self):
        self.engine = sa.create_engine('sqlite:///' + self.get_zip_db_file())
        meta = sa.MetaData(bind=self.engine)
        self.zip_tbl = sa.Table('simple_zipcode', meta, autoload=True)

    def test_extrema(self):
        exclude = 'AK HI PR'.split()
        sess = orm.sessionmaker(bind=self.engine)()
        q = (sess.query(fn.min(self.zip_tbl.c.lat).label('min_lat'),
                        fn.min(self.zip_tbl.c.lng).label('min_lng'),
                        fn.max(self.zip_tbl.c.lat).label('max_lat'),
                        fn.max(self.zip_tbl.c.lng).label('max_lng'),
                        )
             .filter(~self.zip_tbl.c.state.in_(exclude))
             )
        min_lat, min_lng, max_lat, max_lng = q.one()
        self.assertEqual(24.6, min_lat)
        self.assertEqual(-124.62, min_lng)
        self.assertEqual(49.3, max_lat)
        self.assertEqual(-67.02, max_lng)

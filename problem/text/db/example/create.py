#! /usr/bin/env python

# Copyright 2020 John Hanley.
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

from contextlib import closing
from pathlib import Path
import time
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as orm


class RandomIoTest:

    # A million rows corresponds to ~ 4 GiB, produced within 3 minutes.
    def __init__(self, num_rows=1e6, db_fspec='/tmp/big.db'):
        self.num_rows = int(num_rows)
        self.db_fspec = Path(db_fspec)
        self.engine = sa.create_engine(
            self._get_connect_string(self.db_fspec))

    @staticmethod
    def _get_connect_string(fspec):
        return f'sqlite:///{fspec}'

    def create_if_needed(self):
        if self.db_fspec.exists():
            return
        self.engine.execute(self._get_create())
        meta = sa.MetaData(bind=self.engine)
        lstg = sa.Table('listing', meta, autoload=True)
        batch_size = int(self.num_rows / 1e2)  # A hundred batches, each with many rows.
        n = 0
        with closing(orm.session.sessionmaker(bind=self.engine)()) as sess:
            while n < self.num_rows:
                rows = [dict(id=n + i,
                             guid=str(uuid.uuid4()))
                        for i in range(batch_size)]
                ins = lstg.insert().values(rows)
                sess.execute(ins)
                sess.commit()
                n += len(rows)
                print('.', end='', flush=True)

            # Finish with blind update, bulking up all rows.
            sess.execute(self._get_update(),
                         params=self._get_params())
            sess.commit()
            print('.')

    def _get_create(self):
        return """
            CREATE TABLE listing (
                id            INTEGER  PRIMARY KEY,
                guid          TEXT  UNIQUE,
                price         INTEGER,
                full_address  TEXT,
                desc1         TEXT,
                desc2         TEXT,
                desc3         TEXT,
                desc4         TEXT
            )
        """

    @staticmethod
    def _get_update():
        return sa.text("""
            UPDATE listing
            SET    price = :price,
                   full_address = :full_address,
                   desc1 = :desc1,
                   desc2 = :desc2,
                   desc3 = :desc3,
                   desc4 = :desc4
        """)

    HOME_PRICE = 100_000

    @classmethod
    def _get_params(cls):
        lorem = cls._de_finibus_bonorum_et_malorum()
        return dict(
            price=cls.HOME_PRICE,
            full_address='1 Main St, Springfield MA 01101',
            desc1=lorem,
            desc2=lorem,
            desc3=lorem,
            desc4=lorem,
        )

    @staticmethod
    def _de_finibus_bonorum_et_malorum():
        return """
Sed ut perspiciatis unde omnis iste natus error sit voluptatem
accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae
ab illo inventore veritatis et quasi architecto beatae vitae dicta
sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos
qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed
quia non numquam eius modi tempora incidunt ut labore et dolore magnam
aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum
exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex
ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in
ea voluptate velit esse quam nihil molestiae consequatur, vel illum
qui dolorem eum fugiat quo voluptas nulla pariatur?
        """.strip()

    def read_sequential_simple(self):
        # Reads 1e6 rows in ~ 12s.
        select = """
            SELECT   SUM(price)
            FROM     listing
        """
        return self.engine.execute(select).first()[0] / self.HOME_PRICE

    def read_sequential(self):
        # Reads 1e6 rows within 16s.
        return self.read_rows(tuple(i
                              for i in range(self.num_rows)))

    def read_rows(self, all_ids):
        n = total = 0
        batch_size = int(self.num_rows / 1e2)
        sess = orm.sessionmaker(bind=self.engine)()
        while n < self.num_rows:
            # Sigh! Sqlite IN won't accept bind params.
            ids = all_ids[n:n + batch_size]
            select = f"""
                SELECT   SUM(price)
                FROM     listing
                WHERE    id in {ids}
            """
            total += sess.execute(select).first()[0]
            n += batch_size
            print('.', end='', flush=True)
        print('')
        return total / self.HOME_PRICE


if __name__ == '__main__':
    rit = RandomIoTest()
    rit.create_if_needed()

    t0 = time.time()
    assert rit.num_rows == rit.read_sequential()
    print(round(time.time() - t0, 3))

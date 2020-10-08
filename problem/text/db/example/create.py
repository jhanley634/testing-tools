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

from pathlib import Path

import sqlalchemy as sa


class RandomIoTest:

    def __init__(self, db_fspec='/tmp/big.db'):
        self.db_fspec = Path(db_fspec)
        self.engine = sa.create_engine(
            self._get_connect_string(self.db_fspec))

    @staticmethod
    def _get_connect_string(fspec):
        return f'sqlite:///{fspec}'

    def create(self):
        if self.db_fspec.exists():
            return
        lorem = self._de_finibus_bonorum_et_malorum()
        self.engine.execute(self._get_create())

    def _get_create(self):
        return """
            CREATE TABLE listing (
                id            INTEGER  PRIMARY KEY,
                price         INTEGER,
                full_address  TEXT,
                desc1         TEXT,
                desc2         TEXT,
                desc3         TEXT,
                desc4         TEXT
            )
        """

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


if __name__ == '__main__':
    rit = RandomIoTest()
    rit.create()

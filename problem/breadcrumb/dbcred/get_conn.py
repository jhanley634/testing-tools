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

import configparser
import os
import sqlalchemy
import sqlalchemy.orm

SESSION = sqlalchemy.orm.scoped_session(
          sqlalchemy.orm.sessionmaker())


def get_cem(section, cfg_file='~/.db_cred.ini'):
    '''
    Gets connection, (db) engine, and meta data, based on section of cfg_file.
    Each database server has its own config section,
    sometimes multiple sections in order to supply different user credentials.
    '''
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser(cfg_file))
    params = [cfg[section][name]
              for name in 'user password server db'.split()]
    cs = 'mysql://%s:%s@%s/%s' % (tuple(params))  # JDBC connect string
    engine = sqlalchemy.create_engine(cs)  # at end, could engine.dispose()
    SESSION.remove()
    SESSION.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return engine.connect(), engine, sqlalchemy.MetaData(bind=engine)

# Example .db_cred.ini config file, accessed with get_cem('demo'):
#
# ; A small test instance.
# [demo]
# user = scott
# password = tiger
# server = localhost
# db = test

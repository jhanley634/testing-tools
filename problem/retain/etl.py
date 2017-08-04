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
import csv
import datetime
import os
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Table, Column, DATE, DECIMAL, INTEGER, VARCHAR
from sqlalchemy.orm import scoped_session, sessionmaker

Base = sqlalchemy.ext.declarative.declarative_base()
Session = scoped_session(sessionmaker())


class Order(Base):
    __tablename__ = 's_order'
    order_date = Column('order_date', DATE())
    category_name = Column('category_name', VARCHAR(length=80))
    product_name = Column('product_name', VARCHAR(length=80))
    order_sequence = Column('order_sequence', INTEGER())
    revenue = Column('revenue', DECIMAL(precision=9, scale=2))
    units = Column('units', INTEGER())
    customer_id = Column('customer_id', INTEGER())
    order_id = Column('order_id', INTEGER(), primary_key=True)


def get_db_connection(section='retain', cfg_file='~/.db_cred.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser(cfg_file))
    params = [cfg[section][name]
              for name in 'user password server db'.split()]
    cs = 'mysql://%s:%s@%s/%s' % (tuple(params))  # JDBC connect string
    engine = sqlalchemy.create_engine(cs)  # at end, could engine.dispose()
    Session.remove()
    Session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine.connect(), engine, sqlalchemy.MetaData(bind=engine)


def get_row_chunks(csv_fspec, n=8000):
    with open(csv_fspec) as fin:
        reader = csv.DictReader(fin, delimiter=',')
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) >= n:
                yield chunk
                chunk = []
        if len(chunk) > 0:
            yield chunk


def round_to_cent(n, k=100):
    return round(n * k) / k


def parse_dd_mon_yy(dd_mon_yy, fmt='%d-%b-%y'):
    '''Returns iso8601, e.g. 2-Jan-14 -> 2014-01-02.'''
    # https://imgs.xkcd.com/comics/iso_8601.png
    dt = datetime.datetime.strptime(dd_mon_yy, fmt)
    return str(dt).split()[0]


def etl(table_name):
    '''Reads from .CSV in current directory, writes it into mysql.'''
    db, engine, meta = get_db_connection()
    order = Table('s_order', meta, autoload=True, autoload_with=engine)
    order.delete().execute()
    # db.execute('delete from ' + table_name)

    for chunk in get_row_chunks(table_name + '.csv'):
        for row in chunk:
            row['revenue'] = round_to_cent(float(row['revenue']))
            row['order_date'] = parse_dd_mon_yy(row['order_date'])
            row['order_id'] = None  # Sadly, input data is unusable.

        # Throughput over TCP to mysql server is ~11k row/sec.
        engine.execute(Order.__table__.insert(), chunk)

    Session.commit()


if __name__ == '__main__':
    os.chdir('/tmp')
    etl('s_order')

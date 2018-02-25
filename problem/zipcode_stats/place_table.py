
# autogen'd from: sqlacodegen --noclasses sqlite:////tmp/places.db
# create unique index st_nm_idx on place(state, name);

# coding: utf-8
from sqlalchemy import Column, Float, Index, Integer, MetaData, String, Table


metadata = MetaData()


t_places = Table(
    'place', metadata,
    Column('state', String(2)),
    Column('fips', String(7)),
    Column('name', String(64)),
    Column('pop2k', Integer),
    Column('homes2k', Integer),
    Column('lat', Float, index=True),
    Column('lng', Float, index=True),
    Index('st_nm_idx', 'state', 'name', unique=True)
)

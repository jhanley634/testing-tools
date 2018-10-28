#! /usr/bin/env python3

import math
import os

import folium
import sqlalchemy as sa
import sqlalchemy.orm as orm
import uszipcode


class PopDensityFinder:
    """Returns zipcode population figures, as inhabitants per square mile."""

    def __init__(self, db_fspec='/tmp/simple_db.sqlite'):  # DB from uszipcode
        self.engine = sa.create_engine(f'sqlite:///{db_fspec}')
        meta = sa.MetaData(bind=self.engine)
        self.zip_tbl = sa.Table('simple_zipcode', meta, autoload=True)

    def get_pops(self, ul, lr, min_area=1):
        c = self.zip_tbl.c
        # We require that the ZIP's bounding box fit entirely between ul & lr.
        q = (orm.sessionmaker(bind=self.engine)()
             .query(c.population_density,
                    c.major_city,
                    c.zipcode,
                    c.lat,
                    c.lng)
             .filter(lr[0] <= c.bounds_south)  # lower right coord
             .filter(c.bounds_north < ul[0])   # upper left coord
             .filter(ul[1] <= c.bounds_west)
             .filter(c.bounds_east < lr[1])
             .filter(c.land_area_in_sqmi >= min_area)
             .filter(c.population_density > 0)
             .order_by(c.population_density.asc()))
        return q.all()


def _clip(n, hi=1e6):
    n = max(200, n)
    return n if n < hi else hi + (n - hi) / 5


def pop_map(fspec='~/Desktop/map.html'):
    map_ = folium.Map(
        location=(37.5, -122.5),
        tiles='Stamen Terrain',
    )
    # map_.add_child(folium.LatLngPopup())

    for pop_dens, name, zipcode, lat, lng in PopDensityFinder().get_pops(
            (38, -123), (36, -121)):
        folium.Circle(
            radius=10 * math.sqrt(_clip(pop_dens)),
            location=[lat, lng],
            popup=f'{name} {zipcode}, &nbsp; {round(pop_dens / 1e3, 1)} k',
            color='crimson',
            fill=False,
        ).add_to(map_)

    map_.save(os.path.expanduser(fspec))


def menlo():
    search = uszipcode.SearchEngine(simple_zipcode=False)
    result = search.by_zipcode('94025')
    assert f'{result.major_city}, CA' == result.post_office_city


if __name__ == '__main__':
    menlo()
    pop_map()

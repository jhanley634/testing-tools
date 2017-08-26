
OUT = \
 TAGS \
 /tmp/ne_110m_admin_0_countries.shp \

all: $(OUT)

TAGS:
	etags *.py */*.py
	flake8  etl.py */[^_]*.py || true

etl:
	cat schema.sql views.sql | mysql -v -p breadcrumb
	./etl.py

DATA_DIR = https://github.com/mapnik/mapnik/wiki/data/

%.zip:
	wget -nv -O $@ $(DATA_DIR)$(notdir $@)
	touch -m -t 201108190040 $@  # Makes *.shp look up-to-date.

/tmp/ne_110m_admin_0_countries.shp:  /tmp/110m-admin-0-countries.zip
	cd /tmp && time unzip -u $<

clean:
	rm -rf $(OUT) dbcred/__pycache__/

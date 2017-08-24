
OUT = TAGS

all: $(OUT)

TAGS:
	etags *.py */*.py
	flake8  etl.py */[^_]*.py || true

etl:
	cat schema.sql views.sql | mysql -v -p breadcrumb
	./etl.py

clean:
	rm -rf $(OUT) dbcred/__pycache__/

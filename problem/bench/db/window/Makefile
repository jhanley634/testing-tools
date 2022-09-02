
DB = /tmp/window.sqlite
SQL = sqlite3 -header -column $(DB)

all:
	./wave.py | $(SQL)
	cat rank.sql | $(SQL)

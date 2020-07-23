
OUT = /tmp/census.csv /tmp/million.txt

all: $(OUT)

/tmp/census.txt:
	python -m cProfile ./find_matching_zips.py | awk '$$2 > .001'

/tmp/million.txt:
	yes | head -1000000 > $@
	time ./regex1.py  < $@
	time ./regex2.py  < $@

clean:
	rm -f $(OUT)

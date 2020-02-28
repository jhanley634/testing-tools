
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

OUT = \
 cxx_d/mset_cxx \
 /tmp/1.png \
 /tmp/2.png \
 /tmp/3.png \
 /tmp/4.png \

all: $(OUT)

TOP := $(shell git rev-parse --show-toplevel)
ENV = time env PYTHONPATH=$(TOP) MSET_PX_RESOLUTION=500
LOCATION = -.5 0 1  # think four unit squares, centered a bit left of the origin

SO = mset_cython_ext.cpython-37m-darwin.so

/tmp/profile_py3:
	$(ENV) python -m cProfile -o $@ mset.py $(LOCATION) > /dev/null
	echo stats | python -m pstats $@ | sort -nk2 | tail -90
	@echo "   ncalls  tottime  percall  cumtime  percall"

/tmp/profile_numba:
	$(ENV) python -m cProfile -o $@ mset_numba.py $(LOCATION) > /dev/null
	echo stats | python -m pstats $@ | sort -nk2 | tail -90
	@echo "   ncalls  tottime  percall  cumtime  percall"

# 8.2s of laptop user-mode CPU
%1.ppm:
	$(ENV) ./mset.py $(LOCATION) > $@

# 1.2s with sig declarations, 1.7s without
%2.ppm:
	$(ENV) ./mset_numba.py $(LOCATION) > $@

# .53s with sig + cdef declarations, 1.9s with cdef decls, 5.2s without
%3.ppm: cython_d/$(SO)
	cd cython_d && $(ENV) ./mset_cython.py $(LOCATION) > $@

%4.ppm: cxx_d/mset_cxx
	$< $(LOCATION) > $@

%.png: %.ppm
	convert $< $@

cython_d/$(SO): cython_d/mset_cython_ext.pyx
	cd cython_d && python setup.py build_ext --inplace

cxx_d/mset_cxx:
	make -C cxx_d

clean:
	bash -c "rm -rf /tmp/*.ppm cython_d/{build,$(SO)} $(OUT)"

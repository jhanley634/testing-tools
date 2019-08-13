
# Copyright 2019 John Hanley.
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

ENV := /tmp/environment.yml
CUR := /tmp/environment-current.yml

ENV_LIST := $(ENV).txt
CUR_LIST := $(CUR).txt

all: diffs

check:
	cd ../.. && problem/conda_env_yml/env_report.py

$(CUR): $(ENV)
	sed -e '/^name:/s/$$/-current/' -e 's/ *[<>=].*//'  < $? > $@
	diff -wu $? $@ || true

NAME = $(shell awk '/^name:/ {print $$2}' $(CUR))

$(ENV_LIST): $(ENV)
	time conda env update -f $<
	conda list --name $(NAME) | awk '{print $$1; print}' > $@

$(CUR_LIST): $(CUR)
	time conda remove --name $(NAME) --all --yes
	time conda env update -f $<
	conda list --name $(NAME)-current | awk '{print $$1; print}' > $@

diffs: $(ENV_LIST) $(CUR_LIST)
	diff -wu $? || true

clean:
	rm -f $(CUR) $(CUR_LIST) $(ENV_LIST)

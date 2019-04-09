
ENV := /tmp/environment.yml
CUR := /tmp/environment-current.yml

ENV_LIST := $(ENV).txt
CUR_LIST := $(CUR).txt

all: diffs

$(CUR): $(ENV)
	sed -e '/^name:/s/$$/-current/' -e 's/ *[<>=].*//'  < $? > $@
	diff -wu $? $@ || true

NAME = $(shell awk '/^name:/ {print $$2}' $(CUR))

$(ENV_LIST): $(ENV)
	time conda env update -f $<
	conda list | awk '{print $$1; print}' > $@

$(CUR_LIST): $(CUR)
	time conda remove --name $(NAME) --all --yes
	time conda env update -f $<
	conda list | awk '{print $$1; print}' > $@

diffs: $(ENV_LIST) $(CUR_LIST)
	diff -wu $? || true

clean:
	rm -f $(CUR) $(CUR_LIST) $(ENV_LIST)

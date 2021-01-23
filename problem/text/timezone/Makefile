
OUT = \
 timezone.html \
 timezone.pdf \

all: $(OUT)

%.html: %.md
	pandoc -o $@ $<

%.pdf: %.md
	pandoc -o $@ $<

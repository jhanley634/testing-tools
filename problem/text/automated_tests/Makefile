
OUT = \
 testing.html \
 testing.pdf \

all: $(OUT)

%.html: %.md
	pandoc -o $@ $<

%.pdf: %.md
	pandoc --pdf-engine=xelatex -o $@ $<

clean:
	rm -f $(OUT)

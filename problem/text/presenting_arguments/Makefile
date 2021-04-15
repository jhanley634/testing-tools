
OUT = \
 on_writing_code_for_humans.html \
 on_writing_code_for_humans.pdf \

all: $(OUT)

HEADER = ../reviewing/header.tex
ENGINE = --pdf-engine=xelatex

%.html: %.md
	pandoc -o $@ $<

%.pdf: %.md
	pandoc -t beamer -H $(HEADER) $(ENGINE) -o $@ $<

clean:
	rm -f $(OUT)

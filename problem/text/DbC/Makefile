
OUT = \
 design_by_contract.html \
 design_by_contract.pdf \

all: $(OUT)

%.html: %.md
	pandoc -o $@ $<

%.pdf: %.md
	pandoc --pdf-engine=xelatex -o $@ $<

clean:
	rm -f $(OUT)

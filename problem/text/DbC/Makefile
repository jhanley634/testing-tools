
OUT = \
 design_by_contract.html \
 design_by_contract.pdf \

all: $(OUT)

%.html: %.md
	pandoc -o $@ $<

%.pdf: %.md
	pandoc -o $@ $<

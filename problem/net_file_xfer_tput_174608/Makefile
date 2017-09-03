
# Copyright 2017 John Hanley.
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
 observed_throughput.txt \
 /tmp/b2a_tsg.xpl \

all: $(OUT)

observed_throughput.txt: show_chunk_throughput.py
	./$< > $@

/tmp/b2a_tsg.xpl: /tmp/packets2
	cd /tmp && tcptrace -S -zy -l $< && rm -f a2b_tsg.xpl && ls -l $@
	@echo Now run: xplot.org /tmp/b2a_tsg.xpl
	@echo "see also: tcpdump -c 100 -r /tmp/packets2 | egrep --color '192.168.0.20.11057|sack '"

clean:
	rm -f $(OUT)

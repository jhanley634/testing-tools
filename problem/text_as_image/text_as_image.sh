#! /usr/bin/env bash

# Copyright 2018 John Hanley.
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

## Rasterizes input text via HTML rendering to produce an output PNG.

need_download() {
  echo ''
  echo 'Please run:'
  echo '    $ brew install wkhtmltopdf'
  echo "or install binaries from https://wkhtmltopdf.org/downloads.html"
  echo ''
  exit 1
}

wkhtmltoimage --version > /dev/null || need_download

DIR=`dirname $0`
TTOOLS=`cd $DIR/../.. && pwd`
export PYTHONPATH="${PYTHONPATH}:${TTOOLS}"
MOD=problem.text_as_image.text_as_image
NOISE='Loading page .1/2.|Rendering .2/2.|Done'

OUT=~/Desktop/text.png  # default output filespec

if [ _ = _"$1" ]
then
    python3 -m ${MOD} --help; echo ''
    NOISE=no_filtering
else
    OUT=/non/existant.png  # Silent if user specified any options.
fi

python3 -m ${MOD} "$@" | egrep -v "${NOISE}"

test -f ${OUT} && file ${OUT}

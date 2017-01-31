#! /usr/bin/env bash

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


DIR=${1:-no_dest_dir_specified}
PKG=${2:-no_package_specified}
set -e
test -d $DIR

# A file listing of the package's contents.
LISTING=$DIR/pkg/$PKG.txt

set -x

dpkg -L $PKG > $LISTING

src/store_file_names.jl $DIR/pkg_contents.sqlite $LISTING

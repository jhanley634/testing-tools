#! /usr/bin/env julia

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


# usage:
#     src/file_source /some/path [ more paths ...]
#
# Output shall be one of "DEB pkg_name", "URL url", or "UNKNOWN".


using SQLite


function file_source(db, qpath)
    sel = "select src, pkg  from file_source  where pathname = ?"
    return get(SQLite.query(db, sel; values=[qpath])[1, 2])
end


qpath, = ARGS  # the filepath we are querying
db = SQLite.DB("/tmp/file_source/pkg_contents.sqlite")
src = file_source(db, qpath)
println(src)

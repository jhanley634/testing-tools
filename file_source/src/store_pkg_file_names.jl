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
#     src/store_file_names.jl db file_listing


using SQLite

function create_tables(db)
    create = "create table file_source(pathname  string primary key, src  string not null, pkg string)"
    SQLite.query(db, create)
    tbls = SQLite.tables(db)
    println(tbls)
end

function store(db, listing)
    SQLite.transaction(db)
    ins = SQLite.Stmt(db, "insert into file_source  values (?, 'DEB', ?)")
    SQLite.bind!(ins, 2, pkg_name(listing))
    open(listing) do fin
        for line in eachline(fin)
            fspec = rstrip(line)
            if ! isfile(fspec)
                continue
            end
            SQLite.bind!(ins, 1, fspec)
            SQLite.execute!(ins)
        end
    end
    SQLite.commit(db)
end

# "/a/b/c/def.txt" -> "def"
function pkg_name(listing)
    m = match(r".*/([^/]+)\.txt$", listing)
    return m.captures[1]
end


db_fspec, listing = ARGS
if (!isfile(db_fspec))
    create_tables(SQLite.DB(db_fspec))
end
store(SQLite.DB(db_fspec), listing)

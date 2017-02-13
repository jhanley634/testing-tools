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


# Answers the question: "what fraction of my files came from .deb packages?"
#
# usage:
#     src/backup_report.jl


using SQLite


function all_files(fspec)
    uid = ccall((:getuid, "libc"), Int32, ())
    pat = Regex("^([\\d-]+ \\d{2}:\\d{2})\\s+"
                * "([\\.\\d]+)\\s+"
                * "([rwx\\w-]+)\\s+"
                * "([\\w-]+)\\s+"
                * "(\\d+)\\s+"
                * "(\\d+)\\s+"
                * "(.*)")
    Task() do
        open(fspec) do fin
            for line in eachline(fin)
                m = match(pat, rstrip(line))
                if ! (m === nothing)
                    mtime, ctime, perm, owner, links, size, file = m.captures
                    if isfile(file)
                        st = stat(file)
                        # Mine, or world read, or (ordinary) group read.
                        isreadable = (st.uid == uid) ||
                            (stat(file).mode & 0o004) > 0 ||
                            ((stat(file).mode & 0o040) > 0 && !is_security_group(st.gid))
                        if isreadable
                            produce(file)
                        end
                    end
                end
            end
        end
    end
end

function is_security_group(gid)
    return gid == 42 ||  # shadow
        gid == 107       # mlocate
end

function report(db, all_files)
    sel = "select src, pkg" *
        "  from file_source" *
        "  where pathname = ?"

    for file in all_files

        result = SQLite.query(db, sel; values=[file])

        if size(result, 1) == 0
            println(file)
        end
    end
end


dir = "/tmp/file_source/"
db = SQLite.DB(dir * "pkg_contents.sqlite")
report(db, all_files(dir * "find.txt"))

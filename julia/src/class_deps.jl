#! /usr/bin/env julia

# Copyright 2016 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# software.


# usage:
#     $ ./class_deps.jl *.java

using PyCall
@pyimport pydot

import_re = r"^import(\s+static|)\s+([\w\.]*\w)"

function get_edges(src_files)
    Task() do
        for fspec in src_files
            fspec1 = replace(basename(fspec), ".java", "")
            open(fspec) do fin
                for line in readlines(fin)
                    m = match(import_re, line)
                    if m != nothing
                        produce(fspec1, m[2])
                    end
                end
            end
        end
    end
end


ignore_re = r"^(javax?|android|org\.slf4j|com\.google)\.|^org.apache.commons.lang3.(StringUtils|time.FastDateFormat)|\.util\.(Util|LoggerBg|STException)$|\.R$"

function get_filtered_edges(src_files)
    Task() do
        for (src, dst) in get_edges(src_files)
            if !ismatch(ignore_re, dst)
                produce(src, dst)
            end
        end
    end
end


function abbrev(class)
    replace(class, r".*\.", "")
end

function report(out_file, src_files, ignores)
    g = pydot.Dot(rankdir="LR")

    for (src, dst) in get_filtered_edges(src_files)
        println(src, " ", dst)
        e = pydot.Edge(src, abbrev(dst))
        g[:add_edge](e)
    end
    g[:write](out_file)
end

report("/tmp/deps.dot", ARGS, Set())

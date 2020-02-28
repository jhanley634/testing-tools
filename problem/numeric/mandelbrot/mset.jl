#! /usr/bin/env julia

# Copyright 2020 John Hanley.
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


struct PPM

    function PPM(size_px)
        println("P3")
        println(size_px, " ", size_px)
        println("255\n")
    end
end
    function plot(grey_value)
        v = grey_value
        println(v, " ", v, " ", v)
    end


function mandelbrot_set(xc, yc, sz, px_resolution=500)
    PPM(px_resolution)
    step = (2 * sz) / (px_resolution - 1)

    for j in 0 : px_resolution-1
        for i in 0 : px_resolution-1
            x0 = xc - sz + step * i
            y0 = yc - sz + step * j
            plot(_cycles_to_escape(x0, y0, 255))
        end
    end
end


function _cycles_to_escape(x0, y0, max_iter=255)
    x, y, i = 0.0, 0.0, 0
    while x * x + y * y <= 4 && i < max_iter
        x, y = x * x - y * y + x0, 2 * x * y + y0
        i += 1
    end
    return i
end


xc = parse(Float64, ARGS[1])
yc = parse(Float64, ARGS[2])
sz = parse(Float64, ARGS[3])
mandelbrot_set(xc, yc, sz)

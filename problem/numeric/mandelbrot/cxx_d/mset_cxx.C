
// Copyright 2020 John Hanley.
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// The software is provided "AS IS", without warranty of any kind, express or
// implied, including but not limited to the warranties of merchantability,
// fitness for a particular purpose and noninfringement. In no event shall
// the authors or copyright holders be liable for any claim, damages or
// other liability, whether in an action of contract, tort or otherwise,
// arising from, out of or in connection with the software or the use or
// other dealings in the software.

#include <iostream>
using namespace std;

/*
class PPM{
    public:
    PPM(uint size_px);
    void plot(uint grey_value);
};
*/
class PPM {
    public:

    PPM(uint size_px) {
        cout << "P3" << endl;
        cout << size_px << " " << size_px << endl;
        cout << 255 << endl;
    }

    void plot(uint grey_value) {
        int v = grey_value;
        cout << v << " " << v << " " << v << endl;
    }
};

int cycles_to_escape(double x0, double y0, uint max_iter) {
    double x = 0.0;
    double y = 0.0;
    int i = 0;
    while (x * x + y * y <= 4 && i < max_iter) {
        double xt = x;
        x = x * x - y * y + x0;
        y = 2 * xt * y + y0;
        ++i;
    }
    return i;
}

void mandelbrot_set(double xc, double yc, double sz, uint px_resolution) {
    // Given center x,y and a "radius" size, create a square PPM m-set.
    // from https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings
    PPM ppm = PPM(px_resolution);

    double step = (2 * sz) / (px_resolution - 1);

    for (int j=0; j < px_resolution; j++) {
        for (int i=0; i < px_resolution; i++) {
            double x0 = xc - sz + step * i;
            double y0 = yc - sz + step * j;
            // cout << 99 << " " << i << " " << j << " " << x0 << " " << y0 << endl;
            ppm.plot(cycles_to_escape(x0, y0, 255));
        }
    }
}


const char *get_res() {
    char *p = getenv("MSET_PX_RESOLUTION");
    return p ? p : "100";
}

int main(int argc, char *argv[]) {

    if (argc != 4) {
        cerr << "Need 4 args, got: " << argc << endl;
        exit(1);
    }

    float xc = atof(argv[1]);
    float yc = atof(argv[2]);
    float sz = atof(argv[3]);
    uint px_resolution = atoi(get_res());

    mandelbrot_set(xc, yc, sz, px_resolution);
    return 0;
}

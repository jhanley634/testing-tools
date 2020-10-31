
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

#include <chrono>
#include <iostream>
using namespace std;


void bench_cout(const uint n) {
    cout << "cout!" << endl;
}

void bench_printf(const uint n) {
    cout << "printf!" << endl;
}


void usage() {
    cerr << "usage:" << endl;
    cerr << "  Specify --cout or --printf" << endl;
    exit(1);
}
void usage1(const uint n) {
    usage();
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        usage();
    }
    void (*fn)(const uint) = usage1;
    string opt = argv[1];
    if (opt == "--cout") {
        fn = bench_cout;
    } else if (opt == "--printf") {
        fn = bench_printf;
    } else {
        usage();
    }
    chrono::steady_clock::time_point t0 = chrono::steady_clock::now();

    fn(10);

    float elapsed = chrono::duration_cast<chrono::milliseconds>(
         chrono::steady_clock::now() - t0).count() / 1e3;
    cerr << elapsed << " seconds" << endl;
}

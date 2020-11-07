
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

use std::env;

const MAX_ITER: i32 = 255;  // Rust lacks adequate support for default args.

fn mandelbrot_set(xc: f64, yc: f64, sz: f64, px_resolution: i32) {
    let step = (2.0 * sz) / (px_resolution as f64 - 1.0);

    for j in 0 .. px_resolution {
        for i in 0 .. px_resolution {
            let x0 = xc - sz + step * i as f64;
            let y0 = yc - sz + step * j as f64;
            plot(_cycles_to_escape(x0, y0));
        }
    }
}

fn _cycles_to_escape(x0: f64, y0: f64) -> i32 {
    let mut x = 0.0;
    let mut y = 0.0;
    let mut i = 0;
    while x * x + y * y <= 4.0 && i < MAX_ITER {
        let (a, b) = (x * x - y * y + x0, 2.0 * x * y + y0);
        x = a;
        y = b; // rust lacks tuple unpack, aka destructuring assignment
        i += 1;
        // println!("{} {} {} {} {}", x0, y0, i, x, y);
    }
    return i;
}

fn plot(grey_value: i32) {
    let v = grey_value;
    println!("{} {} {}", v, v, v);
}


fn getenv(key: &str) -> i32 {
    let s: String;
    match env::var(key) {
        Ok(v) => s = v,
        Err(_) => s = "400".to_string()
    }
    return stoi(s);
}

fn stoi(s: String) -> i32 {
    return s.parse::<i32>().unwrap();
}

fn stof(s: String) -> f64 {
    return s.parse::<f64>().unwrap();
}

fn main() {
    let px_resolution = getenv("MSET_PX_RESOLUTION");
    let args: Vec<String> = env::args().into_iter().collect();
    let xc = stof(args[1].to_string());
    let yc = stof(args[2].to_string());
    let sz = stof(args[3].to_string());

    println!("P3\n{} {}\n255", px_resolution, px_resolution);
    mandelbrot_set(xc, yc, sz, px_resolution);
}


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

fn _cycles_to_escape(x0: f64, y0: f64) -> i32 {
    let x = 0.0;
    let y = 0.0;
    let mut i = 0;
    while x * x + y * y <= 4.0 && i < MAX_ITER {
        let (x, y) = (x * x - y * y + x0, 2.0 * x * y + y0);
        i += 1;
    }
    return i;
}

fn getenv(key: &str) -> f64 {
    let s: String;
    match env::var(key) {
        Ok(v) => s = v,
        Err(_) => s = "400".to_string()
    }
    return stof(s);
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

    println!("P3\n{} {}\n255", sz, sz);
    println!("{}", _cycles_to_escape(xc, yc));
}

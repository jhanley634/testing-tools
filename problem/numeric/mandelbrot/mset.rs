
use std::env;

fn get1(key: &str) -> String {
    return env::var(key).unwrap();
}

fn get2(key: &str) -> String {
    let ret: String;
    match env::var(key) {
        Ok(v) => ret = v,
        Err(_) => ret = "400".to_string()
    }
    return ret;
}

fn main() {
    for argument in env::args() {
        println!("{}", argument);
    }

    println!("{}", get1("MSET_PX_RESOLUTION"));
    println!("{}", get2("MSET_PX_RESOLUTION"));
}

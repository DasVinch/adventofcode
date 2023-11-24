use std::fs;

pub fn filereader(file_path: &str) -> String {
    println!("Reading file {} from Rust!", file_path);
    fs::read_to_string(file_path).expect("Oh no file reading fucked up.")
}
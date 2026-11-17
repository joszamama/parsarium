//! AFL++ file-input target; feedback comes only from the allowlisted minimp3 C functions.
use parsarium_mp3_minimp3_harness::parse;
fn main() {
    let mut args = std::env::args().skip(1);
    let (Some(path), None) = (args.next(), args.next()) else { std::process::exit(2) };
    if let Ok(data) = std::fs::read(path) {
        let _ = parse(&data);
    }
}

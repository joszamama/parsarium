#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_png_rusty_png_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_zip_tinyzip_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_mp4_oxideav_mp4_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

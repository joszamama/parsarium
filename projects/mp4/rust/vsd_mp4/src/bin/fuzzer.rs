#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_mp4_vsd_mp4_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

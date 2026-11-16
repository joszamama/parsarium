#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_mp4_symphonia_format_isomp4_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

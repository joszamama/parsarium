#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_mp3_symphonia_bundle_mp3_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

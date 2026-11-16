#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_ascii_pnm_bevy_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

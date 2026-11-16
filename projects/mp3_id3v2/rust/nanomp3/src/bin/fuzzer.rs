#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_mp3_id3v2_nanomp3_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

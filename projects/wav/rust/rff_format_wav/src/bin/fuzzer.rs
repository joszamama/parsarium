#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_wav_rff_format_wav_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

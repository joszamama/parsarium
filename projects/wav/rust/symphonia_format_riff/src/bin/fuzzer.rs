#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_wav_symphonia_format_riff_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

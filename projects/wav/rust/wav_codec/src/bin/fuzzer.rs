#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_wav_wav_codec_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_http11_async_http_codec_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

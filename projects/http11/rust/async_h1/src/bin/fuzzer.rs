#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_http11_async_h1_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

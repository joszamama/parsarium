#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_json_simd_json_harness::parse;
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});

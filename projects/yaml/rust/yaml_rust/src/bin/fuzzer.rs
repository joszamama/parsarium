#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_yaml_yaml_rust_harness::parse;
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});

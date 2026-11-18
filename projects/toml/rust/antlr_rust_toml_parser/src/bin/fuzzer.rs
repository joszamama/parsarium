#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_toml_antlr_rust_toml_parser_harness::parse;
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});

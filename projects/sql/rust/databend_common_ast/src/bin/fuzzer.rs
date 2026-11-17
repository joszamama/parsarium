#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_sql_databend_common_ast_harness::parse;
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});

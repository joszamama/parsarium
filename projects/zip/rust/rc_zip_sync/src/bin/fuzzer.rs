#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_zip_rc_zip_sync_harness::parse;
fuzz_target!(|data: &[u8]| { let _ = parse(data); });

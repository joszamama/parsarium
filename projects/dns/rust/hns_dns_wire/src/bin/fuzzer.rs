#![no_main]
use libfuzzer_sys::fuzz_target;
use parsarium_dns_hns_dns_wire_harness::parse;
fuzz_target!(|data: &[u8]| {
    let _ = parse(data);
});

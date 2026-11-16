#![no_main]

use libfuzzer_sys::fuzz_target;
use std::io::Cursor;

fuzz_target!(|data: &[u8]| {
    if data.len() > (1 << 20) {
        return;
    }
    let mut source = Cursor::new(data);
    let _ = metabeam_core::parse(&mut source, data.len() as u64);
});

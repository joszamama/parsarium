use parsarium_ascii_pnm_roka_qr_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

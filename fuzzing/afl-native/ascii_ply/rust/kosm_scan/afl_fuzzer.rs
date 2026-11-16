use parsarium_ascii_ply_kosm_scan_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

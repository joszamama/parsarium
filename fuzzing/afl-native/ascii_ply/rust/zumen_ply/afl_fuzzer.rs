use parsarium_ascii_ply_zumen_ply_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

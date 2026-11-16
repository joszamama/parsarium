use parsarium_ascii_ply_ferrum_cloud_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

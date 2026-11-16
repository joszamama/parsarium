use parsarium_mp4_shiguredo_mp4_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

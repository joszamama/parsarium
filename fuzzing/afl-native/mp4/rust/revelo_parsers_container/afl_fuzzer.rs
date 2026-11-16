use parsarium_mp4_revelo_parsers_container_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

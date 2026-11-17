use parsarium_mp3_symphonium_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

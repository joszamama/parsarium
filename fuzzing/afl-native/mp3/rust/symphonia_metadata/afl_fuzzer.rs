use parsarium_mp3_symphonia_metadata_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

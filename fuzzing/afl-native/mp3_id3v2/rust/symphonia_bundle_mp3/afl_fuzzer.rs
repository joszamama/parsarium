use parsarium_mp3_id3v2_symphonia_bundle_mp3_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

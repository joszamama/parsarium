use parsarium_mp3_id3v2_minimp3_fixed_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

use parsarium_mp4_symphonia_format_isomp4_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

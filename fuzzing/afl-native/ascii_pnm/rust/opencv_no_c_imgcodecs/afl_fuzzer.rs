use parsarium_ascii_pnm_opencv_no_c_imgcodecs_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

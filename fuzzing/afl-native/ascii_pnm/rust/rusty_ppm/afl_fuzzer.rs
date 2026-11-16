use parsarium_ascii_pnm_rusty_ppm_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

use parsarium_svg_svg_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

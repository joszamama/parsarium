use parsarium_svg_ps_anyrender_svg_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

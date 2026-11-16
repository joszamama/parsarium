use parsarium_ascii_ply_brepkit_io_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

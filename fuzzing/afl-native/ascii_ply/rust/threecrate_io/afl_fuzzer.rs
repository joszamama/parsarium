use parsarium_ascii_ply_threecrate_io_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

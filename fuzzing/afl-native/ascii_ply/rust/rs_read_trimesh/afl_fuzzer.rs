use parsarium_ascii_ply_rs_read_trimesh_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

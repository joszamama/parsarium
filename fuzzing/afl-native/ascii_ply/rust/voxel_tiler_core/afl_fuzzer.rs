use parsarium_ascii_ply_voxel_tiler_core_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| { let _ = parse(data); });
}

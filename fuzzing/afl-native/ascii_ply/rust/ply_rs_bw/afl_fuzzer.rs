use parsarium_ascii_ply_ply_rs_bw_harness::parse;

fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

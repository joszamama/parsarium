use parsarium_ascii_pnm_image_harness::parse;

fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

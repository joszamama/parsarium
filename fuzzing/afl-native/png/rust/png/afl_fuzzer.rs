use parsarium_png_crate_harness::parse;

fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

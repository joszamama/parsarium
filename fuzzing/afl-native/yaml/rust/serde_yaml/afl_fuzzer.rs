use parsarium_yaml_serde_yaml_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

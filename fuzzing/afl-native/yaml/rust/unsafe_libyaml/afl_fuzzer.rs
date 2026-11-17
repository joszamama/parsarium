use parsarium_yaml_unsafe_libyaml_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

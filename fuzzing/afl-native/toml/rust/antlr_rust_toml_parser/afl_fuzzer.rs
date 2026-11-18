use parsarium_toml_antlr_rust_toml_parser_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

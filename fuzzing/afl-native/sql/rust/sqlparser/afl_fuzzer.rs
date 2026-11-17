use parsarium_sql_sqlparser_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

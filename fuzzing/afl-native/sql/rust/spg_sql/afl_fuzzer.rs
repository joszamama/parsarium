use parsarium_sql_spg_sql_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

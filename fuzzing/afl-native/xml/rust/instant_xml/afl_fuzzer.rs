use parsarium_xml_instant_xml_harness::parse;
fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

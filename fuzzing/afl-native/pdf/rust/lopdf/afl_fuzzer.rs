use parsarium_pdf_lopdf_harness::parse;

fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

use parsarium_http11_httparse_harness::parse;

fn main() { afl::fuzz!(|data: &[u8]| {
    let _ = parse(data);
});
}

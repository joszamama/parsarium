# uppsala — Rust XML

- **Release:** `uppsala` 0.12.1, BSD-2-Clause; [pinned crate](https://static.crates.io/crates/uppsala/uppsala-0.12.1.crate) and [source lock](../../../../projects/xml/rust/uppsala/source-lock.json)
- **Adoption:** 287,733 crates.io recent downloads in the saved 90-day Rust XML search snapshot
- **Local API:** [`uppsala::parse_bytes(&[u8])`](https://docs.rs/uppsala/0.12.1/uppsala/fn.parse_bytes.html) returns a namespace-aware DOM
- **Family:** Its own pure-Rust XML scanner, recursive-descent parser, namespace resolver, and DOM, with no runtime parser dependency
- **Runnable target:** [Docker harness, exact controls, source coverage, and parser-only AFL++ feedback](../../../../projects/xml/rust/uppsala/README.md)

The two valid namespace controls match the independent Expat oracle for expanded names, ordered attributes, namespace declarations, and decoded text. The AFL++ overlay restricts instrumentation to uppsala and records stable input-dependent edges. This is a verified candidate for the Rust XML selection review; the ten-path ceiling is not padded.

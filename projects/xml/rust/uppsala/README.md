# uppsala — XML / Rust

Pinned release: `0.12.1`. [Manifest](manifest.json) · [Docker control receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/xml/rust/uppsala/verification.json)

The harness passes one local byte buffer to the documented `uppsala::parse_bytes(&[u8])` API. It reads the returned DOM's expanded element and attribute names, namespace declarations, decoded text, and CDATA in document order. Both valid controls match the independent Expat summary from `controls/xml/check_controls.py` exactly.

## Run from the repository root

```sh
python3 parsarium.py build xml rust uppsala
python3 parsarium.py run xml rust uppsala controls/xml/catalog-ns.xml
python3 parsarium.py run xml rust uppsala controls/xml/order-default-ns.xml
python3 parsarium.py afl build xml rust uppsala
python3 parsarium.py afl prepare xml rust uppsala runs/xml-uppsala-afl
```

The pinned Docker control covers 909 lines of uppsala source, including 234 in `src/parser.rs`, 365 in `src/pull.rs`, and 57 in `src/namespace.rs`. The AFL++ overlay instruments **only the uppsala crate**: its build checks that uppsala alone has SanitizerCoverage guards, leaving the harness, serde_json, and other crates uninstrumented. Three valid-control `afl-showmap` runs each were identical: 1,114 edges on the catalog control and 1,285 on the order control, with 94 and 265 edges unique to each respectively. Source coverage also differs in `src/parser.rs` (234 versus 304 lines) and `src/pull.rs` (365 versus 381 lines). The controls do not prove complete XML conformance. No malformed-input or campaign test was run.

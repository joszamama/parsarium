# json (json-rust) — JSON / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid RFC 8259 JSON controls; the cell search remains open.

- **Pinned release:** `json` `0.12.4`; [source crate](https://static.crates.io/crates/json/json-0.12.4.crate), SHA-256 `078e285eafdfb6c4b434e0d31e8cfcb5115b651496faca5749b88fafd4f23bfd`.
- **License:** MIT OR Apache-2.0; both release license files are hashed in [source-lock.json](../../../../projects/json/rust/json_crate/source-lock.json).
- **Parser family:** json-rust's own `src/parser.rs` and `JsonValue` tree. The harness uses `serde_json` only to encode the observed summary, not to parse the input.
- **Local input API:** [`json::parse(&str)`](https://docs.rs/json/0.12.4/json/fn.parse.html), supplied with UTF-8 text decoded from local bytes.
- **Adoption proxy:** 2,672,413 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), ranked only against verified Rust JSON paths.
- **Valid controls:** [`nested-object.json`](../../../../controls/json/nested-object.json) and [`nested-array.json`](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/json_crate/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/json/rust/json_crate/verification.json).

## Observed structure

The adapter reports root type, object and array counts, boolean and null counts, nesting depth, decoded strings and numbers, and top-level keys. The first control produced:

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1.0,
    1.0,
    2.0,
    2.0
  ],
  "objects": 5,
  "root": "object",
  "strings": [
    "café \"quoted\"",
    "go",
    "json",
    "parsarium",
    "rfc8259"
  ],
  "top_level_keys": [
    "enabled",
    "missing",
    "name",
    "nested",
    "ratio",
    "tags",
    "version"
  ]
}
```

The second control has an array root and a different structure; its exact expected output is pinned in the [manifest](../../../../projects/json/rust/json_crate/manifest.json).

## Run this target

```sh
python3 parsarium.py build json rust json_crate
python3 parsarium.py run json rust json_crate controls/json/nested-object.json
python3 parsarium.py afl build json rust json_crate
python3 parsarium.py afl prepare json rust json_crate runs/json-json_crate-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and json-rust parser source coverage.

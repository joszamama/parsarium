# simd-json — JSON / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid RFC 8259 JSON controls; the cell search remains open.

- **Pinned release:** `0.19.0`; [source crate](https://static.crates.io/crates/simd-json/simd-json-0.19.0.crate), SHA-256 `e8f2e4d523646f7da6dde3983bd18ede0babc21c258ab708b3dd93ea0259719d`
- **License:** MIT OR Apache-2.0; both license files are hashed in [source-lock.json](../../../../projects/json/rust/simd_json/source-lock.json).
- **Parser family:** simd-json Rust SIMD/SWAR port of simdjson; its own stage1/stage2 and `OwnedValue` DOM. Its default serde integration is disabled in this harness. `serde_json` encodes the summary only.
- **Local input API:** [`simd_json::to_owned_value(&mut [u8])`](https://docs.rs/simd-json/0.19.0/simd_json/fn.to_owned_value.html), which mutates the local byte buffer and returns an owned tree.
- **Adoption proxy:** 6,730,588 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), ranked only against other verified Rust JSON paths.
- **Valid controls:** [`nested-object.json`](../../../../controls/json/nested-object.json) and [`nested-array.json`](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/simd_json/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/json/rust/simd_json/verification.json).

## Observed structure

The parser returns its own DOM; the adapter reports the root type, object and array counts, boolean and null counts, container depth, decoded strings, numeric values and top-level keys. The first control produced:

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

The second control has an array root and a different structure; its exact expected result is pinned in the [manifest](../../../../projects/json/rust/simd_json/manifest.json).

## Run this target

```sh
python3 parsarium.py build json rust simd_json
python3 parsarium.py run json rust simd_json controls/json/nested-object.json
python3 parsarium.py afl build json rust simd_json
python3 parsarium.py afl prepare json rust simd_json runs/json-simd_json-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate uses only the two valid controls and checks repeated feedback plus parser source coverage.

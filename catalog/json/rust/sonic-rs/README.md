# sonic-rs — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.5.11`
- **Upstream:** [source repository](<https://github.com/cloudwego/sonic-rs>) · [crates.io](<https://crates.io/crates/sonic-rs>)
- **License:** Apache-2.0
- **Parser family:** sonic-rs SIMD JSON parser and own arena-backed Value DOM, with sonic-simd/sonic-number dependencies; separate implementation from serde_json and simd-json, with documented simdjson/other code references
- **Local input API:** `sonic_rs::from_slice::<sonic_rs::Value>(&[u8]); Value::as_ref() -> ValueRef; Object::iter(); Array::iter(); JsonNumberTrait::as_f64()`
- **Documentation:** [API reference](<https://docs.rs/sonic-rs/0.5.11/sonic_rs/fn.from_slice.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/sonic_rs/verification.json)

## Observed control result

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

## Run this target

```sh
python3 parsarium.py build json rust sonic_rs
python3 parsarium.py run json rust sonic_rs controls/json/nested-object.json
```

# serde_json — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.154`
- **Upstream:** [source repository](<https://github.com/serde-rs/json>) · [crates.io](<https://crates.io/crates/serde_json>)
- **License:** MIT OR Apache-2.0
- **Parser family:** serde_json recursive-descent deserializer (serde-rs/json)
- **Local input API:** `serde_json::from_slice::<serde_json::Value>(&[u8]); serde_json::Value::{Object, Array, String, Number, Bool, Null}; Number::as_f64(); Map::keys()`
- **Documentation:** [API reference](<https://docs.rs/serde_json/1.0.154/serde_json/fn.from_slice.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/serde_json/verification.json)

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
python3 parsarium.py build json rust serde_json
python3 parsarium.py run json rust serde_json controls/json/nested-object.json
```

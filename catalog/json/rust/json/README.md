# json — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.12.4`
- **License:** MIT OR Apache-2.0
- **Parser family:** json-rust 0.12.4 own parser.rs and JsonValue tree (maciejhirsz/json-rust); no serde_json parse dependency
- **Local input API:** `json::parse(&str) -> Result<json::JsonValue>; JsonValue::{Object, Array, Short, String, Number, Boolean, Null}; JsonValue::entries()/as_f64()/as_str()`
- **Documentation:** [API reference](<https://docs.rs/json/0.12.4/json/fn.parse.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/json_crate/verification.json)

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
python3 parsarium.py build json rust json_crate
python3 parsarium.py run json rust json_crate controls/json/nested-object.json
```

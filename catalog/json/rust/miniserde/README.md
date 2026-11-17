# miniserde — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.46`
- **License:** MIT OR Apache-2.0
- **Parser family:** miniserde independent non-recursive JSON deserializer in src/json/de.rs and own Value visitor; by serde_json author but no serde_json input parser dependency
- **Local input API:** `miniserde::json::from_str::<miniserde::json::Value>(&str) -> Result<Value>; Value::{Object, Array, String, Number, Bool, Null}`
- **Documentation:** [API reference](<https://docs.rs/miniserde/0.1.46/miniserde/json/fn.from_str.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/miniserde/verification.json)

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
python3 parsarium.py build json rust miniserde
python3 parsarium.py run json rust miniserde controls/json/nested-object.json
```

# gjson — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.8.1`
- **Upstream:** [source repository](<https://github.com/tidwall/gjson.rs>) · [crates.io](<https://crates.io/crates/gjson>)
- **License:** MIT
- **Parser family:** tidwall GJSON path-query family: separate Rust gjson.rs implementation with same maintainer and path syntax as Go tidwall/gjson; Rust source owns its valid.rs validator and lib.rs lazy scanner
- **Local input API:** `gjson::valid(&str) -> bool; gjson::parse(&str) -> Value; Value::each(callback) and Value::{kind,str,f64,json} traverse all children`
- **Documentation:** [API reference](<https://docs.rs/gjson/0.8.1/gjson/fn.parse.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/gjson/verification.json)

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
python3 parsarium.py build json rust gjson
python3 parsarium.py run json rust gjson controls/json/nested-object.json
```

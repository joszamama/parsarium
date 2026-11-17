# jiter — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19.0`
- **License:** MIT
- **Parser family:** Jiter Rust JSON parser (pydantic/jiter); shared underlying parser family with Python pydantic-core 2.50.4 / Jiter 0.18.0, but this standalone Rust path pins Jiter 0.19.0
- **Local input API:** `jiter::JsonValue::parse(&[u8], allow_inf_nan=false) -> Result<JsonValue, JsonError>; JsonValue::{Object, Array, Str, Int, BigInt, Float, Bool, Null}`
- **Documentation:** [API reference](<https://docs.rs/jiter/0.19.0/jiter/enum.JsonValue.html#method.parse>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/jiter/verification.json)

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
python3 parsarium.py build json rust jiter
python3 parsarium.py run json rust jiter controls/json/nested-object.json
```

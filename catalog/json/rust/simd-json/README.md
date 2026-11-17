# simd-json — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19.0`
- **License:** MIT OR Apache-2.0
- **Parser family:** simd-json Rust SIMD/SWAR port of simdjson; own Deserializer stage1/stage2 and OwnedValue DOM, distinct from serde_json parser
- **Local input API:** `simd_json::to_owned_value(&mut [u8]) -> Result<OwnedValue>; OwnedValue::{Object, Array, String, Static}`
- **Documentation:** [API reference](<https://docs.rs/simd-json/0.19.0/simd_json/fn.to_owned_value.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/simd_json/verification.json)

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
python3 parsarium.py build json rust simd_json
python3 parsarium.py run json rust simd_json controls/json/nested-object.json
```

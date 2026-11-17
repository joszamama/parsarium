# json-syntax — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.13.1`
- **License:** MIT OR Apache-2.0
- **Parser family:** json-syntax own strict parser and code map in src/parse; json-number dependency stores numeric lexical form; no serde_json input parser or optional serde_json feature
- **Local input API:** `JsonValue::parse_slice(&[u8]) -> Result<(JsonValue, JsonCodeMap), JsonParseError>`
- **Documentation:** [API reference](<https://docs.rs/json-syntax/0.13.1/json_syntax/parse/trait.JsonParse.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/json_syntax/verification.json)

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
python3 parsarium.py build json rust json_syntax
python3 parsarium.py run json rust json_syntax controls/json/nested-object.json
```

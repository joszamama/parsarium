# aws-smithy-json — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.65.1`
- **Upstream:** [source repository](<https://github.com/smithy-lang/smithy-rs>) · [crates.io](<https://crates.io/crates/aws-smithy-json>)
- **License:** Apache-2.0
- **Parser family:** aws-smithy-json token-stream parser (smithy-rs), used by generated AWS SDK deserializers; own src/deserialize.rs
- **Local input API:** `aws_smithy_json::deserialize::json_token_iter(&[u8]) -> Iterator<Item=Result<Token, DeserializeError>>; Token::{StartObject, EndObject, ObjectKey, StartArray, EndArray, ValueString, ValueNumber, ValueBool, ValueNull}; EscapedStr::to_unescaped()`
- **Documentation:** [API reference](<https://docs.rs/crate/aws-smithy-json/0.65.1/source/src/deserialize.rs>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/aws_smithy_json/verification.json)

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
python3 parsarium.py build json rust aws_smithy_json
python3 parsarium.py run json rust aws_smithy_json controls/json/nested-object.json
```

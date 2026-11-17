# hifijson — JSON / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.5.0`
- **License:** MIT (SPDX declared in release Cargo.toml; no LICENSE file bundled)
- **Parser family:** hifijson independent byte-slice lexer and recursive value parser in src/value.rs, src/token.rs, src/num.rs and src/str.rs; serde_json used only for summary encoding
- **Local input API:** `hifijson::SliceLexer::new(&[u8]); Lex::exactly_one(Lex::ws_peek, |next, lexer| value::parse_bounded(256, next, lexer)) -> Result<Value<_,_>, Error>`
- **Documentation:** [API reference](<https://docs.rs/hifijson/0.5.0/hifijson/struct.SliceLexer.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/rust/json/parsers.json) · [control result](../../../../projects/json/rust/hifijson/verification.json)

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
python3 parsarium.py build json rust hifijson
python3 parsarium.py run json rust hifijson controls/json/nested-object.json
```

# nlohmann-json — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.12.0`
- **License:** MIT
- **Parser family:** nlohmann/json lexer and parser
- **Local input API:** `nlohmann::json::parse(IteratorType first, IteratorType last, parser_callback_t cb = nullptr, bool allow_exceptions = true, bool ignore_comments = false) called on the byte range with allow_exceptions=false and ignore_comments=false`
- **Documentation:** [API reference](<https://json.nlohmann.me/api/basic_json/parse/>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/cpp/json/parsers.json) · [control result](../../../../data/cpp/json/verification.json)

## Observed control result

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1,
    1,
    2,
    2
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
python3 parsarium.py build json cpp nlohmann-json
python3 parsarium.py run json cpp nlohmann-json controls/json/nested-object.json
```

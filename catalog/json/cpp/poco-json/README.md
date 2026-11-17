# POCO JSON — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.15.4`
- **License:** BSL-1.0
- **Parser family:** Poco::JSON::ParserImpl over bundled pdjson C tokenizer
- **Local input API:** `Poco::JSON::Parser::parse(const std::string&) on a local byte-backed std::string; ParseHandler(true) builds an order-preserving Poco::JSON Object or Array DOM`
- **Documentation:** [API reference](<https://docs.pocoproject.org/current/Poco.JSON.Parser.html>)
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
python3 parsarium.py build json cpp poco-json
python3 parsarium.py run json cpp poco-json controls/json/nested-object.json
```

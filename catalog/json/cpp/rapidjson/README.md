# RapidJSON — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.0`
- **Upstream:** [source repository](<https://github.com/Tencent/rapidjson>)
- **License:** MIT (parser headers)
- **Parser family:** RapidJSON header-only SAX/DOM parser
- **Local input API:** `rapidjson::Document::Parse(const char* json, size_t length) over locally supplied bytes; default strict parse flags`
- **Documentation:** [API reference](<https://rapidjson.org/md_doc_tutorial.html>)
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
python3 parsarium.py build json cpp rapidjson
python3 parsarium.py run json cpp rapidjson controls/json/nested-object.json
```

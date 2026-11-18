# PicoJSON — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.3.0`
- **Upstream:** [source repository](<https://github.com/kazuho/picojson>)
- **License:** BSD-2-Clause
- **Parser family:** PicoJSON own header-only recursive-descent parser
- **Local input API:** `picojson::parse(picojson::value&, const std::string&) on local bytes, compiled with the documented PICOJSON_USE_INT64 option so integers stay int64_t and other numbers stay double; objects are std::map with sorted keys`
- **Documentation:** [API reference](<https://github.com/kazuho/picojson/blob/v1.3.0/README.mkdn>)
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
python3 parsarium.py build json cpp picojson
python3 parsarium.py run json cpp picojson controls/json/nested-object.json
```

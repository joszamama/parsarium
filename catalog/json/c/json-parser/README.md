# json-parser — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.0`
- **Upstream:** [source repository](<https://github.com/json-parser/json-parser>) · [Debian](<https://tracker.debian.org/pkg/libjsonparser>)
- **License:** BSD-2-Clause
- **Parser family:** json-parser single-file parser (json.c)
- **Local input API:** `json_parse_ex(json_settings *settings, const json_char *json, size_t length, char *error)`
- **Documentation:** [API reference](<https://github.com/json-parser/json-parser/blob/v1.1.0/README.md>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/c/json/parsers.json) · [control result](../../../../data/c/json/verification.json)

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
python3 parsarium.py build json c json-parser
python3 parsarium.py run json c json-parser controls/json/nested-object.json
```

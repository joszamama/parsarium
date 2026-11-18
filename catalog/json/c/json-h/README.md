# json.h — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `pre-ai`
- **License:** Unlicense
- **Parser family:** json.h header-only parser (sheredom/json.h)
- **Local input API:** `json_parse(const void *src, size_t src_size)`
- **Documentation:** [API reference](<https://github.com/sheredom/json.h/blob/pre-ai/README.md>)
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
python3 parsarium.py build json c json-h
python3 parsarium.py run json c json-h controls/json/nested-object.json
```

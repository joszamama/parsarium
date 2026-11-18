# json-c — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19`
- **Upstream:** [source repository](<https://github.com/json-c/json-c>) · [Debian](<https://tracker.debian.org/pkg/json-c>)
- **License:** MIT
- **Parser family:** json-c incremental state-machine tokener (json_tokener.c)
- **Local input API:** `json_tokener_parse_ex(struct json_tokener *tok, const char *str, int len)`
- **Documentation:** [API reference](<https://json-c.github.io/json-c/json-c-0.19/doc/html/json__tokener_8h.html>)
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
python3 parsarium.py build json c json-c
python3 parsarium.py run json c json-c controls/json/nested-object.json
```

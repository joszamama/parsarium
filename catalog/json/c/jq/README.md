# jq — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.8.2`
- **Upstream:** [source repository](<https://github.com/jqlang/jq>) · [Debian](<https://tracker.debian.org/pkg/jq>)
- **License:** MIT
- **Parser family:** libjq jv parser (src/jv_parse.c)
- **Local input API:** `jv_parse_sized(const char *string, int length) from libjq (jv.h)`
- **Documentation:** [API reference](<https://github.com/jqlang/jq/wiki/C-API:-jv>)
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
python3 parsarium.py build json c jq
python3 parsarium.py run json c jq controls/json/nested-object.json
```

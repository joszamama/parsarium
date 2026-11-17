# yyjson — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.13.0`
- **License:** MIT
- **Parser family:** yyjson native reader (src/yyjson.c)
- **Local input API:** `yyjson_read(const char *dat, size_t len, yyjson_read_flag flg)`
- **Documentation:** [API reference](<https://github.com/ibireme/yyjson/blob/0.13.0/doc/API.md>)
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
python3 parsarium.py build json c yyjson
python3 parsarium.py run json c yyjson controls/json/nested-object.json
```

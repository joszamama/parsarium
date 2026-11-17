# yajl — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.1.0`
- **License:** ISC
- **Parser family:** yajl own lexer and event parser (yajl_lex.c, yajl_parser.c)
- **Local input API:** `yajl_alloc(const yajl_callbacks *, yajl_alloc_funcs *, void *ctx); yajl_parse(yajl_handle, const unsigned char *jsonText, size_t jsonTextLength); yajl_complete_parse(yajl_handle)`
- **Documentation:** [API reference](<https://github.com/lloyd/yajl/blob/2.1.0/src/api/yajl_parse.h>)
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
python3 parsarium.py build json c yajl
python3 parsarium.py run json c yajl controls/json/nested-object.json
```

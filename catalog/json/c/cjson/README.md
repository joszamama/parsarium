# cjson — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.7.19`
- **Upstream:** [source repository](<https://github.com/DaveGamble/cJSON>) · [Debian](<https://tracker.debian.org/pkg/cjson>)
- **License:** MIT
- **Parser family:** cJSON recursive-descent parser (cJSON.c)
- **Local input API:** `cJSON_ParseWithLengthOpts(const char *value, size_t buffer_length, const char **return_parse_end, cJSON_bool require_null_terminated)`
- **Documentation:** [API reference](<https://github.com/DaveGamble/cJSON/blob/v1.7.19/README.md>)
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
python3 parsarium.py build json c cjson
python3 parsarium.py run json c cjson controls/json/nested-object.json
```

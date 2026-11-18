# jansson — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.15.1`
- **Upstream:** [source repository](<https://github.com/akheron/jansson>) · [Debian](<https://tracker.debian.org/pkg/jansson>)
- **License:** MIT
- **Parser family:** jansson recursive-descent decoder (src/load.c)
- **Local input API:** `json_loadb(const char *buffer, size_t buflen, size_t flags, json_error_t *error)`
- **Documentation:** [API reference](<https://jansson.readthedocs.io/en/latest/apiref.html#c.json_loadb>)
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
python3 parsarium.py build json c jansson
python3 parsarium.py run json c jansson controls/json/nested-object.json
```

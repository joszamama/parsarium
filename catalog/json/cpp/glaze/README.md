# Glaze — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `9.1.0`
- **License:** MIT
- **Parser family:** Glaze own template-based JSON reader
- **Local input API:** `glz::read_json(glz::generic_i64&, std::string) on a local byte-backed std::string, yielding an insertion-ordered generic JSON DOM with signed integer and double alternatives`
- **Documentation:** [API reference](<https://github.com/stephenberry/glaze/blob/v9.1.0/docs/generic-json.md>)
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
python3 parsarium.py build json cpp glaze
python3 parsarium.py run json cpp glaze controls/json/nested-object.json
```

# github.com/tidwall/gjson — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.20.4`
- **Upstream:** [source repository](<https://github.com/tidwall/gjson>) · [pkg.go.dev](<https://pkg.go.dev/github.com/tidwall/gjson>)
- **License:** MIT
- **Parser family:** tidwall/gjson path-query parser
- **Local input API:** `gjson.ValidBytes([]byte) then gjson.ParseBytes([]byte); Result.ForEach traverses objects and arrays`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tidwall/gjson@v1.20.4#ParseBytes>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/go/json/parsers.json) · [control result](../../../../data/go/json/verification.json)

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
python3 parsarium.py build json go github_com_tidwall_gjson
python3 parsarium.py run json go github_com_tidwall_gjson controls/json/nested-object.json
```

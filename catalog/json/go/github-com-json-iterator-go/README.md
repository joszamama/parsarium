# github.com/json-iterator/go — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.1.12`
- **License:** MIT
- **Parser family:** json-iterator Iterator parser
- **Local input API:** `jsoniter.Unmarshal([]byte, interface{})`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/json-iterator/go@v1.1.12#Unmarshal>)
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
python3 parsarium.py build json go github_com_json_iterator_go
python3 parsarium.py run json go github_com_json_iterator_go controls/json/nested-object.json
```

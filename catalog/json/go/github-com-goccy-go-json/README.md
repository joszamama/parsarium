# github.com/goccy/go-json — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.12.0`
- **Upstream:** [source repository](<https://github.com/goccy/go-json>) · [pkg.go.dev](<https://pkg.go.dev/github.com/goccy/go-json>)
- **License:** MIT
- **Parser family:** go-json compiled decoder
- **Local input API:** `gojson.Unmarshal([]byte, interface{})`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/goccy/go-json@v0.12.0#Unmarshal>)
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
python3 parsarium.py build json go github_com_goccy_go_json
python3 parsarium.py run json go github_com_goccy_go_json controls/json/nested-object.json
```

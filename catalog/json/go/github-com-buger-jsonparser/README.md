# github.com/buger/jsonparser — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.6.1`
- **License:** MIT
- **Parser family:** buger/jsonparser byte scanner
- **Local input API:** `jsonparser.Get([]byte) plus ObjectEach and ArrayEachErr over local byte slices`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/buger/jsonparser@v1.6.1#Get>)
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
python3 parsarium.py build json go github_com_buger_jsonparser
python3 parsarium.py run json go github_com_buger_jsonparser controls/json/nested-object.json
```

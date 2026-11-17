# github.com/bytedance/sonic — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.15.5`
- **License:** Apache-2.0
- **Parser family:** Sonic optimized arm64 decoder: Go optdec over native NEON parser
- **Local input API:** `sonic.Unmarshal([]byte, *any) over one complete local JSON byte slice`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/bytedance/sonic@v1.15.5#Unmarshal>)
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
python3 parsarium.py build json go github_com_bytedance_sonic
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-object.json
```

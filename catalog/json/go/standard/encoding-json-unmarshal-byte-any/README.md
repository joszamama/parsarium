# encoding/json.Unmarshal([]byte, any) — JSON / Go

**Pilot / incomplete format cell.**

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Parser family:** Go encoding/json v2 / jsontext decoder
- **Official documentation:** [reference](https://pkg.go.dev/encoding/json@go1.27.1#Unmarshal)
- **Valid control:** [`controls/json/nested-object.json`](../../../../../controls/json/nested-object.json)
- **Inventory:** [standard API record](../../../../../data/go/json/standard.json) · [saved result](../../../../../projects/json/go/stdlib_unmarshal/verification.json)

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
python3 parsarium.py build json go stdlib_unmarshal
python3 parsarium.py run json go stdlib_unmarshal controls/json/nested-object.json
```

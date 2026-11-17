# github.com/segmentio/encoding/json — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.5.4`
- **License:** MIT
- **Parser family:** segmentio/encoding/json own Go parser (parseValue + reflection codec)
- **Local input API:** `json.Unmarshal([]byte, *any) over one complete local JSON byte slice`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/segmentio/encoding/json@v0.5.4#Unmarshal>)
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

## Verification scope

Both valid controls (nested-object.json and nested-array.json) match exact structural summaries recomputed with Python's json module as an independent oracle. The object control covers 367 lines in five files of the pinned json package (parse.go 217, decode.go 106, codec.go 23, json.go 17, int.go 4). AFL++ feedback is scoped to the json package: 273 parser features and 293 tuples on the object control; repeats of each control are identical, and the array control changes 14 parser features and 14 tuples. The module zip and the segmentio/asm v1.1.3 dependency zip are sha256-checked in the Dockerfile. pkg.go.dev Imported by 348 comes from the same 2026-11-17 snapshot as the other Go JSON rows and was rechecked at 2026-11-17T14:34Z.

## Run this target

```sh
python3 parsarium.py build json go segmentio_encoding
python3 parsarium.py run json go segmentio_encoding controls/json/nested-object.json
```

# github.com/go-faster/jx — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.2.0`
- **License:** MIT
- **Parser family:** go-faster/jx own Go decoder (lightweight fork of json-iterator)
- **Local input API:** `jx.DecodeBytes([]byte) Decoder walked with Next/Obj/Arr/Str/Float64/Bool/Null over one complete local JSON byte slice; a final Skip must return io.EOF`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-faster/jx@v1.2.0#DecodeBytes>)
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

Both valid controls (nested-object.json and nested-array.json) match exact structural summaries recomputed with Python's json module as an independent oracle. The object control covers 355 lines in twelve files of the pinned jx package (dec_str.go 120, dec_float.go 76, dec_read.go 35, dec_obj.go 30, dec.go 24, dec_arr.go 18, dec_float_big.go 13, dec_bool.go 12, dec_null.go 8, w_int.gen.go 7 from the package init digit table, dec_depth.go 6, dec_skip.go 6). AFL++ feedback is scoped to the jx package: 222 parser features and 242 tuples on the object control; repeats of each control are identical, and the array control changes 38 parser features and 38 tuples. The jx v1.2.0 module zip and the go-faster/errors v0.7.1 and segmentio/asm v1.2.1 dependency zips are sha256-checked in the Dockerfile. pkg.go.dev Imported by 451 comes from the same 2026-11-17 snapshot as the other Go JSON rows and was rechecked at 2026-11-17T15:03Z.

## Run this target

```sh
python3 parsarium.py build json go github_com_go_faster_jx
python3 parsarium.py run json go github_com_go_faster_jx controls/json/nested-object.json
```

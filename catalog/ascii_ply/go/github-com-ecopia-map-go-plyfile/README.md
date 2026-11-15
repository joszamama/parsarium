# github.com/ecopia-map/go-plyfile — ASCII PLY / Go

- **Pinned release:** `v1.0.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex count and coordinate
- **Underlying family:** Greg Turk plyfile C family
- **Local input API:** `PlyOpenForReading(string); PlyGetElement(CPlyFile, interface{}, uintptr)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ecopia-map/go-plyfile@v1.0.0>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "last": {
    "X": 0,
    "Y": 1,
    "Z": 0
  }
}
```

Go wrapper fork over the same Greg Turk C PLY parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

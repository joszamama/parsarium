# github.com/unixpickle/model3d/fileformats — ASCII PLY / Go

- **Pinned release:** `v0.4.23`
- **License:** BSD-2-Clause
- **Parsed scope:** ASCII PLY vertex and face counts
- **Underlying family:** model3d PLY
- **Local input API:** `NewPLYReader(io.Reader); PLYReader.Read()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unixpickle/model3d@v0.4.23/fileformats>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

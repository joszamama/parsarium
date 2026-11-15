# github.com/NOT-REAL-GAMES/assimpgo — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20260306134222-05660fb62c9d`
- **License:** MIT
- **Parsed scope:** ASCII PLY mesh, vertex, and face counts
- **Underlying family:** Assimp C++ importer
- **Local input API:** `ImportFile(string, PostProcessFlags)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/NOT-REAL-GAMES/assimpgo@v0.0.0-20260306134222-05660fb62c9d>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3,
  "faces": 1
}
```

Go wrapper or fork over Assimp; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

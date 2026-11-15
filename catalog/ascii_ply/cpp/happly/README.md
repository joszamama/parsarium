# happly — ASCII PLY / C++

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** three parsed vertices and one triangular face from ASCII PLY
- **Underlying family:** hapPLY header-only PLY parser
- **Local input API:** `happly::PLYData(local filename); getVertexPositions(); getFaceIndices()`
- **Documentation:** [API reference](<https://github.com/nmwsharp/happly/blob/v1.1.0/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

Independent header-only C++ PLY parser, not an alias of Assimp or OpenMesh.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

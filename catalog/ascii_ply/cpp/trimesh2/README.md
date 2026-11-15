# trimesh2 — ASCII PLY / C++

- **Pinned release:** `2022.03.04`
- **License:** GPL-2.0-only
- **Parsed scope:** three vertices and one triangle face with parsed indices from ASCII PLY
- **Underlying family:** TriMesh2 native PLY reader
- **Local input API:** `trimesh::TriMesh::read(local filename)`
- **Documentation:** [API reference](<https://github.com/Forceflow/trimesh2/blob/2022.03.04/README.md>)
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

TriMesh2 parses PLY in its own TriMesh_io.cc; this Forceflow release is a fork of Szymon Rusinkiewicz TriMesh2.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

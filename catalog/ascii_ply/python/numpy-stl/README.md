# numpy-stl — ASCII PLY / Python

- **Pinned release:** `4.1.3`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** numpy-stl PLY reader
- **Local input API:** `stl.mesh.Mesh.from_ply_file(path)`
- **Documentation:** [API reference](<https://pypi.org/project/numpy-stl/>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_ply/parsers.json) · [control verification](../../../../data/python/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertex_count": 3,
  "face_count": 1,
  "first_vertex": [
    0.0,
    0.0,
    0.0
  ],
  "last_vertex": [
    0.0,
    1.0,
    0.0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

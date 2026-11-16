# pymeshlab — ASCII PLY / Python

- **Pinned release:** `2025.7.post1`
- **License:** GPL-3.0
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** MeshLab PLY reader
- **Local input API:** `MeshSet.load_new_mesh(path); current_mesh()`
- **Documentation:** [API reference](<https://pymeshlab.readthedocs.io/en/latest/classes/meshset.html>)
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

## Verified Docker control

[Control harness and receipt](../../../../projects/ascii_ply/python/pymeshlab/README.md)

The pinned valid control parses successfully in Docker. Native parser source coverage and AFL++ feedback are unavailable for this path, so it remains staged.

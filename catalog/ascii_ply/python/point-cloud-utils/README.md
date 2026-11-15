# point-cloud-utils — ASCII PLY / Python

- **Pinned release:** `0.34.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** point-cloud-utils native PLY reader
- **Local input API:** `point_cloud_utils.load_mesh_vf(path)`
- **Documentation:** [API reference](<https://pypi.org/project/point-cloud-utils/>)
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

# pyntcloud — ASCII PLY / Python

- **Pinned release:** `0.3.1`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** pyntcloud PLY reader
- **Local input API:** `PyntCloud.from_file(path)`
- **Documentation:** [API reference](<https://pypi.org/project/pyntcloud/>)
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

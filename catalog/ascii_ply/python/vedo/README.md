# vedo — ASCII PLY / Python

- **Pinned release:** `2026.6.3`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** VTK PLYReader
- **Local input API:** `vedo.load(path)`
- **Documentation:** [API reference](<https://vedo.embl.es/site/api/file_io/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/vedo/README.md)

```sh
python3 parsarium.py build ascii_ply python vedo
python3 parsarium.py run ascii_ply python vedo controls/ascii_ply/triangle.ply
```

# libigl — ASCII PLY / Python

- **Pinned release:** `2.6.3`
- **License:** MPL-2.0
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** libigl PLY reader
- **Local input API:** `igl.read_triangle_mesh(path)`
- **Documentation:** [API reference](<https://libigl.github.io/libigl-python-bindings/api/igl/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/libigl/README.md)

```sh
python3 parsarium.py build ascii_ply python libigl
python3 parsarium.py run ascii_ply python libigl controls/ascii_ply/triangle.ply
```

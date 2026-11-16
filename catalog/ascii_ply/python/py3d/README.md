# py3d — ASCII PLY / Python

- **Pinned release:** `0.1.92`
- **License:** GPL-3.0
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** py3d PLY reader
- **Local input API:** `py3d.read_ply(path)`
- **Documentation:** [API reference](<https://tumiz.github.io/py3d/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/py3d/README.md)

```sh
python3 parsarium.py build ascii_ply python py3d
python3 parsarium.py run ascii_ply python py3d controls/ascii_ply/triangle.ply
```

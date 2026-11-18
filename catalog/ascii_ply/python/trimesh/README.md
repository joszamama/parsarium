# trimesh — ASCII PLY / Python

- **Pinned release:** `5.2.0`
- **Upstream:** [source repository](<https://github.com/mikedh/trimesh>) · [PyPI](<https://pypi.org/project/trimesh/>)
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** trimesh PLY loader
- **Local input API:** `trimesh.load(path, force="mesh")`
- **Documentation:** [API reference](<https://trimesh.org/trimesh.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/trimesh/README.md)

```sh
python3 parsarium.py build ascii_ply python trimesh
python3 parsarium.py run ascii_ply python trimesh controls/ascii_ply/triangle.ply
```

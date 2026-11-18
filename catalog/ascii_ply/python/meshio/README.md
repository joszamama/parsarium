# meshio — ASCII PLY / Python

- **Pinned release:** `5.3.5`
- **Upstream:** [source repository](<https://github.com/nschloe/meshio>) · [PyPI](<https://pypi.org/project/meshio/>)
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** meshio PLY reader
- **Local input API:** `meshio.read(path)`
- **Documentation:** [API reference](<https://github.com/nschloe/meshio>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/meshio/README.md)

```sh
python3 parsarium.py build ascii_ply python meshio
python3 parsarium.py run ascii_ply python meshio controls/ascii_ply/triangle.ply
```

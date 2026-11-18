# vtk — ASCII PLY / Python

- **Pinned release:** `9.7.2`
- **Upstream:** [PyPI](<https://pypi.org/project/vtk/>)
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle vertices and face count
- **Underlying family:** VTK PLYReader
- **Local input API:** `vtk.vtkPLYReader.SetFileName(path); Update(); GetOutput()`
- **Documentation:** [API reference](<https://vtk.org/doc/nightly/html/classvtkPLYReader.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/python/vtk/README.md)

```sh
python3 parsarium.py build ascii_ply python vtk
python3 parsarium.py run ascii_ply python vtk controls/ascii_ply/triangle.ply
```

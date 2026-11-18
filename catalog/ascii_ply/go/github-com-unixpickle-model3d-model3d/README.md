# github.com/unixpickle/model3d/model3d — ASCII PLY / Go

- **Pinned release:** `v0.4.23`
- **Upstream:** [source repository](<https://github.com/unixpickle/model3d>) · [pkg.go.dev](<https://pkg.go.dev/github.com/unixpickle/model3d/model3d>)
- **License:** BSD-2-Clause
- **Parsed scope:** ASCII PLY with x/y/z (optional red/green/blue) vertices and a vertex_index triangle face list, returned as triangles and a vertex colour map
- **Underlying family:** model3d mesh reader over the model3d fileformats PLYReader (shared model3d PLY parser family)
- **Local input API:** `model3d.ReadColorPLY(io.Reader) ([]*Triangle, *CoordMap[[3]uint8], error)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unixpickle/model3d@v0.4.23/model3d#ReadColorPLY>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle-vertex-index.ply`](../../../../controls/ascii_ply/triangle-vertex-index.ply)

## Observed control result

```json
{
  "triangles": 1,
  "first_triangle": [
    [
      0,
      0,
      0
    ],
    [
      1,
      0,
      0
    ],
    [
      0,
      1,
      0
    ]
  ],
  "coloured_vertices": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_unixpickle_model3d_model3d/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_unixpickle_model3d_model3d
python3 parsarium.py run ascii_ply go github_com_unixpickle_model3d_model3d controls/ascii_ply/triangle-vertex-index.ply
```

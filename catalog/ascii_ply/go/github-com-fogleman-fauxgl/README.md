# github.com/fogleman/fauxgl — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20250110135958-abf826acbbbd`
- **Upstream:** [source repository](<https://github.com/fogleman/fauxgl>) · [pkg.go.dev](<https://pkg.go.dev/github.com/fogleman/fauxgl>)
- **License:** MIT
- **Parsed scope:** ASCII PLY header, vertex x/y/z rows and vertex_indices face rows converted to a triangle mesh
- **Underlying family:** fauxgl native Go PLY reader (ply.go)
- **Local input API:** `fauxgl.LoadPLY(path) (*Mesh, error); Mesh.Triangles`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/fogleman/fauxgl@v0.0.0-20250110135958-abf826acbbbd#LoadPLY>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

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
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_fogleman_fauxgl/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_fogleman_fauxgl
python3 parsarium.py run ascii_ply go github_com_fogleman_fauxgl controls/ascii_ply/triangle.ply
```

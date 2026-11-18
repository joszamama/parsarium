# go.viam.com/rdk/spatialmath — ASCII PLY / Go

- **Pinned release:** `v1.17.0`
- **Upstream:** [source repository](<https://github.com/viamrobotics/rdk>) · [pkg.go.dev](<https://pkg.go.dev/go.viam.com/rdk/spatialmath>)
- **License:** AGPL-3.0
- **Parsed scope:** ASCII PLY triangle faces converted to millimetre-scaled triangles
- **Underlying family:** Viam RDK spatialmath mesh loader over goply (shared goply parser family)
- **Local input API:** `spatialmath.NewMeshFromPLYFile(path); (*Mesh).Triangles()`
- **Documentation:** [API reference](<https://pkg.go.dev/go.viam.com/rdk@v1.17.0/spatialmath#NewMeshFromPLYFile>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "triangles": 1,
  "first_triangle_mm": [
    [
      0,
      0,
      0
    ],
    [
      1000,
      0,
      0
    ],
    [
      0,
      1000,
      0
    ]
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/go_viam_com_rdk_spatialmath/README.md)

```sh
python3 parsarium.py build ascii_ply go go_viam_com_rdk_spatialmath
python3 parsarium.py run ascii_ply go go_viam_com_rdk_spatialmath controls/ascii_ply/triangle.ply
```

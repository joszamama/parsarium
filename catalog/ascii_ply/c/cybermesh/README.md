# cybermesh — ASCII PLY / C

- **Pinned release:** `0.5.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY three parsed vertices, one triangle, coordinate and face indices
- **Underlying family:** CyberMeshGenerator native ASCII PLY reader through its C ABI
- **Local input API:** `cmg_read_plc(local .ply path); cmg_plc_num_points; cmg_plc_num_triangles; cmg_plc_points; cmg_plc_triangles`
- **Documentation:** [API reference](<https://github.com/CyberdyneCorp/CyberMeshGenerator/blob/v0.5.0/bindings/c/include/cmg_c/cmg_c.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "vertex_1_x": 1.0,
  "face": [
    0,
    1,
    2
  ]
}
```

The C ABI wraps the project's C++ ASCII PLY parser. This is a released package path but has no comparable Homebrew metric; GitHub stars at review time were zero and are only auxiliary project-interest evidence.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

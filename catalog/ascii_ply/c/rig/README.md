# rig — ASCII PLY / C

- **Pinned release:** `2`
- **License:** LGPL-2.1-or-later; bundled RPly MIT
- **Parsed scope:** One valid ASCII PLY triangle; unmodified tagged parser with mesh/GPU support replaced by observation-only stand-ins
- **Underlying family:** Rig Rut PLY loader over bundled RPly 1.01
- **Local input API:** `rut_mesh_new_from_ply(RutContext*, local filename, position attributes, status, GError**) returns RutMesh with parsed vertices and triangle indices`
- **Documentation:** [API reference](<https://github.com/rib/rig/blob/2/rut/rut-mesh-ply.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "indices": 3,
  "face": [
    0,
    1,
    2
  ],
  "second_x": 1.0
}
```

Separate tagged C package path, but its PLY syntax parsing uses bundled RPly 1.01, so it is not an independent parser engine from RPly or BRL-CAD. Full Cogl/Rut graphics integration is not verified.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

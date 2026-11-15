# geometry-central — ASCII PLY / C++

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** three mesh vertices and one polygon with three indices
- **Underlying family:** Geometry Central SimplePolygonMesh over hapPLY
- **Local input API:** `geometrycentral::surface::SimplePolygonMesh(local filename, "ply")`
- **Documentation:** [API reference](<https://geometry-central.net/surface/utilities/simple_polygon_mesh/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

Tagged Geometry Central v1.1.0 uses pinned hapPLY submodule commit 88f79725; this shares the hapPLY parser family with the standalone happly 1.1.0 path.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

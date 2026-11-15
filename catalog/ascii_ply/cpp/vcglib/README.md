# vcglib — ASCII PLY / C++

- **Pinned release:** `2025.07`
- **License:** GPL-3.0-only
- **Parsed scope:** three vertices and one triangle face with parsed indices from ASCII PLY
- **Underlying family:** VCGlib native plylib parser
- **Local input API:** `vcg::tri::io::ImporterPLY<Mesh>::Open(mesh, local filename)`
- **Documentation:** [API reference](<https://github.com/cnr-isti-vclab/vcglib/blob/2025.07/apps/sample/trimesh_attribute_ply/trimesh_attribute_ply.cpp>)
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

VCGlib ImporterPLY uses its bundled plylib implementation; this is not an alias of TriMesh2 or RPly.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

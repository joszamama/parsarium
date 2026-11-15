# open-mesh — ASCII PLY / C++

- **Pinned release:** `11.0.0`
- **License:** BSD-3-Clause
- **Parsed scope:** three vertices and one triangular face from ASCII PLY
- **Underlying family:** OpenMesh PLYReader
- **Local input API:** `OpenMesh::IO::read_mesh(mesh, local filename)`
- **Documentation:** [API reference](<https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.0-Documentation/a00740.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

OpenMesh uses its own PLYReader and mesh representation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

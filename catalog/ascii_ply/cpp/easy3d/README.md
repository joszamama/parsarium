# easy3d — ASCII PLY / C++

- **Pinned release:** `2.6.1`
- **License:** GPL-3.0-only AND MIT
- **Parsed scope:** three mesh vertices and one triangle face with indices from ASCII PLY
- **Underlying family:** Easy3D PLY reader over bundled RPly 1.1.4
- **Local input API:** `easy3d::SurfaceMeshIO::load(local filename); SurfaceMesh::n_vertices/n_faces/vertices(face)`
- **Documentation:** [API reference](<https://github.com/LiangliangNan/Easy3D/blob/v2.6.1/easy3d/fileio/surface_mesh_io.h>)
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

Easy3D SurfaceMeshIO and PlyReaderWriter use bundled RPly 1.1.4. It exposes a distinct SurfaceMesh API but shares the underlying RPly parser family with RPly, rplycpp, and Geogram.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

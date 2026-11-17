# cgal — ASCII PLY / C++

- **Pinned release:** `6.2.1`
- **License:** GPL-3.0-or-later
- **Parsed scope:** three vertices and one face in a parsed Surface_mesh
- **Underlying family:** CGAL Surface_mesh PLY reader
- **Local input API:** `std::ifstream(local filename); CGAL::IO::read_PLY(stream, Surface_mesh, comments)`
- **Documentation:** [API reference](<https://doc.cgal.org/latest/Surface_mesh/group__PkgSurfaceMeshIOFuncPLY.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

CGAL owns its Surface_mesh PLY import implementation, distinct from Assimp, OpenMesh, hapPLY and tinyply.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/cgal/README.md)

```sh
python3 parsarium.py build ascii_ply cpp cgal
python3 parsarium.py run ascii_ply cpp cgal controls/ascii_ply/triangle.ply
```

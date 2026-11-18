# gmsh — ASCII PLY / C

- **Pinned release:** `4.15.2`
- **Upstream:** [source repository](<https://github.com/gmsh-project/gmsh>) · [Debian](<https://tracker.debian.org/pkg/gmsh>)
- **License:** GPL-2.0-or-later with listed linking exception
- **Parsed scope:** One valid local ASCII PLY triangle; three parsed positions, one triangle and three node references through the C API
- **Underlying family:** Gmsh native PLY reader
- **Local input API:** `gmshInitialize; gmshOpen(local .ply path); gmshModelMeshGetNodes; gmshModelMeshGetElementsByType(2)`
- **Documentation:** [API reference](<https://gmsh.info/doc/texinfo/gmsh.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "triangles": 1,
  "triangle_nodes": 3,
  "x_sum": 1.0
}
```

Gmsh uses its own GModelIO_PLY reader. Its C API calls the C++ implementation in the same released library; this is one package path, independent of the RPly and micro_ply families.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/gmsh/README.md)

```sh
python3 parsarium.py build ascii_ply c gmsh
python3 parsarium.py run ascii_ply c gmsh controls/ascii_ply/triangle.ply
```

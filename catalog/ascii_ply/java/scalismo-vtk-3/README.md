# scalismo-vtk_3 — ASCII PLY / Java

- **Pinned release:** `1.0-RC1`
- **Upstream:** [source repository](<https://github.com/unibas-gravis/scalismo-vtk>) · [Maven Central](<https://central.sonatype.com/artifact/ch.unibas.cs.gravis/scalismo-vtk_3>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle vertices, face list and parsed point ids
- **Underlying family:** VTK vtkPLYReader via the scalismo-vtk Scala binding (VTK 9.1 Java natives)
- **Local input API:** `scalismo.vtk.initialize(false, 0) then scalismo.vtk.io.MeshIO.readMesh(File) on a local .ply path, returning Try[TriangleMesh[_3D]] (point count, triangle count, first triangle point ids)`
- **Documentation:** [API reference](<https://github.com/unibas-gravis/scalismo-vtk/blob/v1.0-RC1/src/main/scala/scalismo/vtk/io/MeshIO.scala>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "indices": [
    0,
    1,
    2
  ]
}
```

scalismo-vtk is a separate unibas-gravis repository and Maven artifact from the selected scalismo_3 (whose 1.0 PLY reader is pure Scala). Its MeshIO.readPLY scans the header in Scala, then parses through VTK's vtkPLYReader from the vtkjavanatives VTK 9.1 Java build; the VTK PLY family is shared with the f3d Java path, so it is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/scalismo_vtk/README.md)

```sh
python3 parsarium.py build ascii_ply java scalismo_vtk
python3 parsarium.py run ascii_ply java scalismo_vtk controls/ascii_ply/triangle.ply
```

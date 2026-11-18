# scalismo_3 — ASCII PLY / Java

- **Pinned release:** `1.0-RC1`
- **Upstream:** [source repository](<https://github.com/unibas-gravis/scalismo>) · [Maven Central](<https://central.sonatype.com/artifact/ch.unibas.cs.gravis/scalismo_3>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle vertices, face list and parsed point ids
- **Underlying family:** Scalismo pure Scala PLY reader (scalismo.io.ply)
- **Local input API:** `scalismo.io.MeshIO.readMesh(File) on a local .ply path, returning Try[TriangleMesh[_3D]] (point count, triangle count, first triangle point ids)`
- **Documentation:** [API reference](<https://github.com/unibas-gravis/scalismo/blob/v1.0-RC1/src/main/scala/scalismo/io/MeshIO.scala>)
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

Scalismo 1.0 replaced its former VTK vtkPLYReader path with its own Scala PLY header, ASCII and binary readers; the release is a Scala 3 JVM artifact callable from Java. scalismo-faces ships a separate Scala PLY reader and records 0 deps.dev dependents.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/scalismo/README.md)

```sh
python3 parsarium.py build ascii_ply java scalismo
python3 parsarium.py run ascii_ply java scalismo controls/ascii_ply/triangle.ply
```

# imglib2-mesh — ASCII PLY / Java

- **Pinned release:** `1.3.0`
- **License:** BSD-2-Clause
- **Parsed scope:** ASCII triangle, three vertices and one face
- **Underlying family:** ImgLib2 Mesh public PLY API over jPLY
- **Local input API:** `PLYMeshIO.open(String local ASCII PLY file path), returning BufferMesh`
- **Documentation:** [API reference](<https://github.com/imglib/imglib2-mesh/blob/imglib2-mesh-1.3.0/src/main/java/net/imglib2/mesh/io/ply/PLYMeshIO.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

Published SciJava mesh library delegates PLY syntax parsing to org.smurn:jply:0.2.1; the jPLY 0.2.0 package path and Jzy3d Core wrapper are separately recorded. This is another package input API, not an independent parser engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

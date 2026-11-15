# imaging-mesh — ASCII PLY / Java

- **Pinned release:** `2.0.0`
- **License:** MPL-2.0
- **Parsed scope:** ASCII triangle, three points and one polygon face
- **Underlying family:** AIST Imaging native ASCII PLY mesh reader
- **Local input API:** `new PlyReader().read(BufferedReader from local ASCII PLY file), returning Optional<JavaModel3D>`
- **Documentation:** [API reference](<https://github.com/FHOOEAIST/imaging/blob/imaging-2.0.0/mesh/src/main/java/science/aist/imaging/mesh/storage/ply/PlyReader.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "points": 3,
  "faces": 1
}
```

Tagged Java source implements its own ASCII PLY header, vertex and face reader; no shared syntax parser with the other included Java paths was found.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# meshio — ASCII PLY / Java

- **Pinned release:** `2.1.2`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex and face counts, parsed face indices
- **Underlying family:** MeshIO native ASCII PLY mesh reader
- **Local input API:** `new PlyFormatAscii_1_0().read(InputStream from local path)`
- **Documentation:** [API reference](<https://github.com/NathanJAdams/MeshIO#using-formats-directly>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

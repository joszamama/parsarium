# irurueta-geometry-io — ASCII PLY / Java

- **Pinned release:** `1.6.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle vertices, face and parsed indices
- **Underlying family:** Irurueta Geometry I/O native Java PLY reader
- **Local input API:** `new LoaderPLY(File local path).load(); iterate DataChunk vertices and face indices`
- **Documentation:** [API reference](<https://www.irurueta.com/irurueta-geometry-io/1.6.0/format-ply.html>)
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

Separate Java implementation; exact-release deps.dev public direct dependents are zero, which does not establish wide adoption.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

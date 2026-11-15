# javagl-ply — ASCII PLY / Java

- **Pinned release:** `0.0.4`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertex and face counts, parsed face indices
- **Underlying family:** JavaGL Ply native Java ASCII PLY reader
- **Local input API:** `PlyReaders.create().read(InputStream from local path), PlySource.getElementList(), Element.getIntListProperty()`
- **Documentation:** [API reference](<https://github.com/javagl/Ply/tree/ply-parent-0.0.4>)
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

# bteterrarenderer-draco — ASCII PLY / Java

- **Pinned release:** `v1.03.4`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle, three parsed vertices, one face and second vertex X coordinate
- **Underlying family:** BTETerraRenderer Java translation of Draco PLY reader
- **Local input API:** `new PlyReader().read(DecoderBuffer initialized from local InputStream); getElementByName and PlyPropertyReader inspect parsed elements and coordinates`
- **Documentation:** [API reference](<https://github.com/tf2mandeokyi/BTETerraRenderer/blob/v1.03.4/draco/src/test/java/com/mndk/bteterrarenderer/draco/io/PlyReaderTest.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "second_x": 1.0
}
```

The draco module translates Draco C++ code into Java; it contains its own PlyReader and is a source-built library module, not a separately observed Maven artifact. Its origin is the Draco parser family; no other Java cell path here uses this Java translation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

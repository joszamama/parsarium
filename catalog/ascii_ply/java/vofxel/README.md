# vofxel — ASCII PLY / Java

- **Pinned release:** `v0.0.2`
- **License:** GPL-3.0
- **Parsed scope:** Eight colored ASCII PLY voxel vertices; first X and red value, last Z coordinate; no faces
- **Underlying family:** Vofxel native Java colored ASCII PLY vertex reader
- **Local input API:** `new PlyParser(InputStream).parse() returns VertexList with coordinate and RGB fields`
- **Documentation:** [API reference](<https://github.com/iAmGio/vofxel/blob/v0.0.2/src/main/java/eu/iamgio/vofxel/PlyParser.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/voxel-rgb.ply`](../../../../controls/ascii_ply/voxel-rgb.ply)

## Observed control result

```json
{
  "vertices": 8,
  "first_x": 0.0,
  "first_red": 255,
  "last_z": 1.0
}
```

Separate Java vertex reader. Its released parser reads six-column coordinate/RGB rows after end_header; it does not expose faces or validate other PLY header fields. No shared underlying parser family was found.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

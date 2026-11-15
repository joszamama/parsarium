# assimp — ASCII PLY / C

- **Pinned release:** `6.0.6`
- **License:** BSD-3-Clause AND CC-PDDC AND MIT AND BSL-1.0 AND Unlicense AND Zlib
- **Parsed scope:** three vertices and one triangular face from ASCII PLY
- **Underlying family:** Assimp native PLY loader
- **Local input API:** `aiImportFile(local filename)`
- **Documentation:** [API reference](<https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

C and C++ Assimp APIs share the same native PLY loader.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

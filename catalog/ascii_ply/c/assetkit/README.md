# assetkit — ASCII PLY / C

- **Pinned release:** `0.7.4`
- **License:** Apache-2.0
- **Parsed scope:** three vertices and one triangular face with parsed indices from ASCII PLY
- **Underlying family:** AssetKit native ASCII PLY importer
- **Local input API:** `ak_load(&doc, local filename, AK_FILE_TYPE_AUTO); ak_meshFromGeometry; ak_meshPrimitiveIndexAccessor`
- **Documentation:** [API reference](<https://github.com/recp/AssetKit/blob/v0.7.4/samples/read_meshes.c>)
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

C and C++ adapters call the same AssetKit C API and native PLY importer.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/assetkit/README.md)

```sh
python3 parsarium.py build ascii_ply c assetkit
python3 parsarium.py run ascii_ply c assetkit controls/ascii_ply/triangle.ply
```

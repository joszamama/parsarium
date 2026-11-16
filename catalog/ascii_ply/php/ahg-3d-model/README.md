# ahg/3d-model — ASCII PLY / PHP

- **Pinned release:** `1.165.35`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PLY header-only parsing: declared vertex and face element counts from a valid local ASCII triangle; no vertex/face body data read
- **Underlying family:** Heratio pure PHP PLY header metadata extractor
- **Local input API:** `Ahg3dModel\Services\ModelMetadataExtractor::extract(local PLY path, "ply") reads header element counts`
- **Documentation:** [API reference](<https://github.com/ArchiveHeritageGroup/heratio/blob/v1.165.35/packages/ahg-3d-model/src/Services/ModelMetadataExtractor.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_ply/parsers.json) · [control verification](../../../../data/php/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

Distinct ahg/3d-model Composer library within the Heratio monorepo. Extracts PLY-specific header counts directly in PHP, without Assimp or Providence code.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/php/ahg_3d_model/README.md)

```sh
python3 parsarium.py build ascii_ply php ahg_3d_model
python3 parsarium.py run ascii_ply php ahg_3d_model controls/ascii_ply/triangle.ply
```

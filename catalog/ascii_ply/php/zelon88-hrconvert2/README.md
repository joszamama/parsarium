# zelon88/hrconvert2 — ASCII PLY / PHP

- **Pinned release:** `v4.0.0`
- **License:** GPL-3.0
- **Parsed scope:** One valid ASCII PLY triangle converted through real PyMeshLab and Assimp stages; OBJ geometry and both stage outputs observed
- **Underlying family:** HRConvert2 PHP Model pipeline over PyMeshLab PLY reader and Assimp exporter
- **Local input API:** `convertModels(local ASCII PLY path, local OBJ output path, "obj"); uses PyMeshLab to load PLY and Assimp to export OBJ`
- **Documentation:** [API reference](<https://github.com/zelon88/HRConvert2/blob/v4.0.0/Resources/Pipelines/Model/pipelineConfig.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_ply/parsers.json) · [control verification](../../../../data/php/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "x_sum": 1.0,
  "completed_stages": 2
}
```

Separate tagged GPL PHP application module; PyMeshLab/MeshLab reads PLY and Assimp exports OBJ. The standalone adapter supplies host-application services and omits the web server sandbox. This is one package path over underlying native readers, not an independent PHP syntax parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

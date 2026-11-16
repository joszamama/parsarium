# online-3d-viewer — ASCII PLY / JavaScript

- **Pinned release:** `0.18.0`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** Online3DViewer PLY importer
- **Local input API:** `new ImporterPly().Import(name, "ply", localArrayBuffer, callbacks)`
- **Documentation:** [API reference](<https://unpkg.com/online-3d-viewer@0.18.0/source/engine/import/importerply.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_ply/parsers.json) · [control verification](../../../../data/javascript/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": [
    [
      0,
      0,
      0
    ],
    [
      1,
      0,
      0
    ],
    [
      0,
      1,
      0
    ]
  ],
  "faces": [
    [
      0,
      1,
      2
    ]
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/online_3d_viewer/README.md)

```sh
python3 parsarium.py build ascii_ply javascript online_3d_viewer
python3 parsarium.py run ascii_ply javascript online_3d_viewer controls/ascii_ply/triangle.ply
```

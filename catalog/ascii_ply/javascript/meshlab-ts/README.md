# meshlab-ts — ASCII PLY / JavaScript

- **Pinned release:** `2026.8.3`
- **Upstream:** [source repository](<https://github.com/yuyakinjo/meshlab-ts>) · [npm](<https://www.npmjs.com/package/meshlab-ts>)
- **License:** GPL-3.0-or-later
- **Parsed scope:** triangle mesh
- **Underlying family:** meshlab-ts PLY reader
- **Local input API:** `readPly(new CMeshO(), localBytes, fileName)`
- **Documentation:** [API reference](<https://unpkg.com/meshlab-ts@2026.8.3/dist/meshlabplugins/io_base/ply.d.ts>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/meshlab_ts/README.md)

```sh
python3 parsarium.py build ascii_ply javascript meshlab_ts
python3 parsarium.py run ascii_ply javascript meshlab_ts controls/ascii_ply/triangle.ply
```

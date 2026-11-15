# ply-js — ASCII PLY / JavaScript

- **Pinned release:** `0.0.4`
- **License:** GPL-3.0-or-later
- **Parsed scope:** triangle mesh
- **Underlying family:** ply-js
- **Local input API:** `readPlyFromLines(localAsciiLines)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/ply-js/v/0.0.4>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# plyparser — ASCII PLY / JavaScript

- **Pinned release:** `6.0.0`
- **License:** ISC
- **Parsed scope:** triangle mesh
- **Underlying family:** plyparser
- **Local input API:** `parsePlyData(localBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/plyparser/v/6.0.0>)
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

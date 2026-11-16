# three — ASCII PLY / JavaScript

- **Pinned release:** `0.187.0`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** Three.js PLYLoader family
- **Local input API:** `new PLYLoader().parse(localArrayBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/three/v/0.187.0>)
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

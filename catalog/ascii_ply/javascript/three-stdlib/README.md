# three-stdlib — ASCII PLY / JavaScript

- **Pinned release:** `2.36.1`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** Three.js PLYLoader family
- **Local input API:** `new PLYLoader().parse(localArrayBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/three-stdlib/v/2.36.1>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/three_stdlib/README.md)

```sh
python3 parsarium.py build ascii_ply javascript three_stdlib
python3 parsarium.py run ascii_ply javascript three_stdlib controls/ascii_ply/triangle.ply
```

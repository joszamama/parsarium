# threejs-ply-loader — ASCII PLY / JavaScript

- **Pinned release:** `1.2.2`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** Three.js PLYLoader family
- **Local input API:** `makeLoader(THREE@0.125.2); new PLYLoader().parse(localArrayBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/threejs-ply-loader/v/1.2.2>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/threejs_ply_loader/README.md)

```sh
python3 parsarium.py build ascii_ply javascript threejs_ply_loader
python3 parsarium.py run ascii_ply javascript threejs_ply_loader controls/ascii_ply/triangle.ply
```

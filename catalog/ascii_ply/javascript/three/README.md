# three — ASCII PLY / JavaScript

- **Pinned release:** `0.187.0`
- **Upstream:** [source repository](<https://github.com/mrdoob/three.js>) · [npm](<https://www.npmjs.com/package/three>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/three/README.md)

```sh
python3 parsarium.py build ascii_ply javascript three
python3 parsarium.py run ascii_ply javascript three controls/ascii_ply/triangle.ply
```

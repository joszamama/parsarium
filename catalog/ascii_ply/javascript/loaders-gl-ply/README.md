# @loaders.gl/ply — ASCII PLY / JavaScript

- **Pinned release:** `4.5.4`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** loaders.gl PLY family
- **Local input API:** `parse(localArrayBuffer, PLYLoader)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@loaders.gl/ply/v/4.5.4>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/loaders_gl_ply/README.md)

```sh
python3 parsarium.py build ascii_ply javascript loaders_gl_ply
python3 parsarium.py run ascii_ply javascript loaders_gl_ply controls/ascii_ply/triangle.ply
```

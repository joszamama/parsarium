# @isopodlabs/binary_meshes — ASCII PLY / JavaScript

- **Pinned release:** `0.1.2`
- **License:** MIT
- **Parsed scope:** triangle mesh
- **Underlying family:** isopodlabs binary_meshes
- **Local input API:** `formatOf(".ply").load(localBytes)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@isopodlabs/binary_meshes/v/0.1.2>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/isopodlabs_binary_meshes/README.md)

```sh
python3 parsarium.py build ascii_ply javascript isopodlabs_binary_meshes
python3 parsarium.py run ascii_ply javascript isopodlabs_binary_meshes controls/ascii_ply/triangle.ply
```

# point-cloud-convert — ASCII PLY / JavaScript

- **Pinned release:** `0.0.3`
- **License:** Apache-2.0
- **Parsed scope:** vertex positions only
- **Underlying family:** point-cloud-convert
- **Local input API:** `pointCloudConvert(localAsciiString, "ply2asc")`
- **Documentation:** [API reference](<https://www.npmjs.com/package/point-cloud-convert/v/0.0.3>)
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
  "faces": []
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

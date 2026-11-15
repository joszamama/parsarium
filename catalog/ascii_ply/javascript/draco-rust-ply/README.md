# @draco-rust/ply — ASCII PLY / JavaScript

- **Pinned release:** `0.3.1`
- **License:** Apache-2.0
- **Parsed scope:** triangle mesh
- **Underlying family:** draco-rust PLY reader
- **Local input API:** `init({module_or_path: localWasmBytes}); read_ply(localBytes)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@draco-rust/ply/v/0.3.1>)
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

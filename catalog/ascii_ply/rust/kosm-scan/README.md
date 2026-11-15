# kosm-scan — ASCII PLY / Rust

- **Pinned release:** `0.0.1`
- **License:** Apache-2.0
- **Parsed scope:** coloured ASCII PLY vertex positions and RGB
- **Underlying family:** kosm-scan ASCII PLY reader
- **Local input API:** `paint::read_colour_cloud(path)`
- **Documentation:** [API reference](<https://docs.rs/kosm-scan/0.0.1/kosm_scan/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle-colour.ply`](../../../../controls/ascii_ply/triangle-colour.ply)

## Observed control result

```json
{
  "vertices": 3,
  "last_colour": [
    0,
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

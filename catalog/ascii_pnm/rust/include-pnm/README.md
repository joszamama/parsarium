# include-pnm — ASCII PNM / Rust

- **Pinned release:** `1.0.0`
- **License:** CC0-1.0
- **Parsed scope:** P3 ASCII PPM RGB pixels at compile time
- **Underlying family:** include-pnm compile-time parser
- **Local input API:** `include_ppm!(supplied_control_path) in a generated build source`
- **Documentation:** [API reference](<https://docs.rs/include-pnm/1.0.0/include_pnm/macro.include_ppm.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
    [
      [
        255,
        0,
        0
      ],
      [
        0,
        255,
        0
      ]
    ]
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

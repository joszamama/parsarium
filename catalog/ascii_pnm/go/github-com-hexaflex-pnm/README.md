# github.com/hexaflex/pnm — ASCII PNM / Go

- **Pinned release:** `v0.0.0-20200810192450-e891a41ac33b`
- **License:** BSD-3-Clause
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** hexaflex PNM
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hexaflex/pnm@v0.0.0-20200810192450-e891a41ac33b>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ],
  "width": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

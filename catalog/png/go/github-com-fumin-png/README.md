# github.com/fumin/png — PNG / Go

- **Pinned release:** `v0.0.0-20220417120418-2266efc3c1a5`
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** Go image/png fork
- **Local input API:** `NewDecoder(io.Reader); DecodeRow()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/fumin/png@v0.0.0-20220417120418-2266efc3c1a5>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ],
  "width": 2
}
```

Shared underlying parser lineage or wrapper; package count is not an independent engine count.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

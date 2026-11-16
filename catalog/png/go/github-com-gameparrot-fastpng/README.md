# github.com/gameparrot/fastpng — PNG / Go

- **Pinned release:** `v0.0.0-20250305185850-d72e123a2123`
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** Go image/png-derived decoder
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gameparrot/fastpng@v0.0.0-20250305185850-d72e123a2123>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/github_com_gameparrot_fastpng/README.md)

```sh
python3 parsarium.py build png go github_com_gameparrot_fastpng
python3 parsarium.py run png go github_com_gameparrot_fastpng controls/png/red-green.png
```

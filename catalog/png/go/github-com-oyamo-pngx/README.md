# github.com/oyamo/pngx — PNG / Go

- **Pinned release:** `v0.0.0-20230307064515-ec4b3bce8a92`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Go image/png fork
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/oyamo/pngx@v0.0.0-20230307064515-ec4b3bce8a92>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_oyamo_pngx/README.md)

```sh
python3 parsarium.py build png go github_com_oyamo_pngx
python3 parsarium.py run png go github_com_oyamo_pngx controls/png/red-green.png
```

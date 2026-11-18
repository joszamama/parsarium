# github.com/fogleman/gg — PNG / Go

- **Pinned release:** `v1.3.0`
- **Upstream:** [source repository](<https://github.com/fogleman/gg>) · [pkg.go.dev](<https://pkg.go.dev/github.com/fogleman/gg>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Go image/png wrapper
- **Local input API:** `LoadPNG(path)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/fogleman/gg@v1.3.0>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_fogleman_gg/README.md)

```sh
python3 parsarium.py build png go github_com_fogleman_gg
python3 parsarium.py run png go github_com_fogleman_gg controls/png/red-green.png
```

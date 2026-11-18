# github.com/go-images/png — PNG / Go

- **Pinned release:** `v0.2.0`
- **Upstream:** [source repository](<https://github.com/go-images/png>) · [pkg.go.dev](<https://pkg.go.dev/github.com/go-images/png>)
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** Go image/png fork
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-images/png@v0.2.0>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_go_images_png/README.md)

```sh
python3 parsarium.py build png go github_com_go_images_png
python3 parsarium.py run png go github_com_go_images_png controls/png/red-green.png
```

# github.com/davidbyttow/govips/v2/vips — PNG / Go

- **Pinned release:** `v2.20.0`
- **Upstream:** [source repository](<https://github.com/davidbyttow/govips>) · [pkg.go.dev](<https://pkg.go.dev/github.com/davidbyttow/govips/v2/vips>)
- **License:** MIT
- **Parsed scope:** dimensions
- **Underlying family:** libvips
- **Local input API:** `NewImageFromFile(path); Width(); Height()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/davidbyttow/govips/v2/vips@v2.20.0>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

Shared underlying parser lineage or wrapper; package count is not an independent engine count.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/github_com_davidbyttow_govips_v2_vips/README.md)

```sh
python3 parsarium.py build png go github_com_davidbyttow_govips_v2_vips
python3 parsarium.py run png go github_com_davidbyttow_govips_v2_vips controls/png/red-green.png
```

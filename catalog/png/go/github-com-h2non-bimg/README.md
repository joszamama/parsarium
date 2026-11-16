# github.com/h2non/bimg — PNG / Go

- **Pinned release:** `v1.1.9`
- **License:** MIT
- **Parsed scope:** dimensions
- **Underlying family:** libvips
- **Local input API:** `Size([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/h2non/bimg@v1.1.9>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_h2non_bimg/README.md)

```sh
python3 parsarium.py build png go github_com_h2non_bimg
python3 parsarium.py run png go github_com_h2non_bimg controls/png/red-green.png
```

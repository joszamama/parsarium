# github.com/go-gfx/gfx/codec — ASCII PNM / Go

- **Pinned release:** `v0.41.0`
- **License:** BSD-3-Clause
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** go-gfx PNM decoder
- **Local input API:** `Decode([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-gfx/gfx/codec@v0.41.0>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_go_gfx_gfx_codec/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_go_gfx_gfx_codec
python3 parsarium.py run ascii_pnm go github_com_go_gfx_gfx_codec controls/ascii_pnm/red-green.ppm
```

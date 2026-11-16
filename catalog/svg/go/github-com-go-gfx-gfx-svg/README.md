# github.com/go-gfx/gfx/svg — SVG / Go

- **Pinned release:** `v0.41.0`
- **License:** BSD-3-Clause
- **Parsed scope:** height, width
- **Underlying family:** go-gfx SVG rasterizer
- **Local input API:** `Rasterize(string, Options).Image`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-gfx/gfx/svg@v0.41.0>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_go_gfx_gfx_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_go_gfx_gfx_svg
python3 parsarium.py run svg go github_com_go_gfx_gfx_svg controls/svg/red-green.svg
```

# github.com/ironpark/ggfx/svg — SVG / Go

- **Pinned release:** `v0.0.0-20261111143539-00f0f2c03daa`
- **License:** Apache-2.0
- **Parsed scope:** height, width
- **Underlying family:** oksvg lineage
- **Local input API:** `Parse(io.Reader).ViewBox()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ironpark/ggfx/svg@v0.0.0-20261111143539-00f0f2c03daa>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

Shared code lineage; package count does not imply independent SVG parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_ironpark_ggfx_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_ironpark_ggfx_svg
python3 parsarium.py run svg go github_com_ironpark_ggfx_svg controls/svg/red-green.svg
```

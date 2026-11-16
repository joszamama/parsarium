# github.com/sfomuseum/go-svg — SVG / Go

- **Pinned release:** `v0.0.0-20231208192434-a3c9facf873c`
- **License:** BSD-3-Clause
- **Parsed scope:** height, width
- **Underlying family:** sfomuseum SVG rasterizer
- **Local input API:** `Rasterize(context.Context, io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/sfomuseum/go-svg@v0.0.0-20231208192434-a3c9facf873c>)
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

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_sfomuseum_go_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_sfomuseum_go_svg
python3 parsarium.py run svg go github_com_sfomuseum_go_svg controls/svg/red-green.svg
```

# github.com/gen2brain/svg — SVG / Go

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parsed scope:** height, width
- **Underlying family:** gen2brain SVG decoder
- **Local input API:** `DecodeConfig(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gen2brain/svg@v0.1.0>)
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

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_gen2brain_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_gen2brain_svg
python3 parsarium.py run svg go github_com_gen2brain_svg controls/svg/red-green.svg
```

# picosvg — SVG / Python

- **Pinned release:** `0.23.0`
- **License:** Apache-2.0
- **Parsed scope:** SVG element tree and dimensions
- **Underlying family:** Google Fonts picosvg tree and simplifier
- **Local input API:** `picosvg.svg.SVG.parse(local_svg_path)`
- **Documentation:** [API reference](<https://github.com/googlefonts/picosvg/blob/v0.23.0/src/picosvg/svg.py>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    "2",
    "1"
  ],
  "rectangles": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/picosvg/README.md)

```sh
python3 parsarium.py build svg python picosvg
python3 parsarium.py run svg python picosvg controls/svg/red-green.svg
```

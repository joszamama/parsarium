# picosvgx — SVG / Python

- **Pinned release:** `0.1.0`
- **License:** Apache-2.0
- **Parsed scope:** SVG element tree and dimensions
- **Underlying family:** picosvg fork (shared underlying picosvg family)
- **Local input API:** `picosvgx.svg.SVG.parse(local_svg_path)`
- **Documentation:** [API reference](<https://pypi.org/project/picosvgx/0.1.0/>)
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

[Docker harness and verification receipt](../../../../projects/svg/python/picosvgx/README.md)

```sh
python3 parsarium.py build svg python picosvgx
python3 parsarium.py run svg python picosvgx controls/svg/red-green.svg
```

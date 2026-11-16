# svgpathtools — SVG / Python

- **Pinned release:** `1.8.0`
- **License:** MIT
- **Parsed scope:** SVG path and shape geometry
- **Underlying family:** svgpathtools SVG path and shape reader
- **Local input API:** `svgpathtools.svg2paths2(local_svg_path)`
- **Documentation:** [API reference](<https://pypi.org/project/svgpathtools/1.8.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-blue-path.svg`](../../../../controls/svg/red-blue-path.svg)

## Observed control result

```json
{
  "paths": 2,
  "width": "4",
  "height": "2",
  "blue_path": "M 2 0 L 4 0 L 4 2 Z"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/svgpathtools/README.md)

```sh
python3 parsarium.py build svg python svgpathtools
python3 parsarium.py run svg python svgpathtools controls/svg/red-blue-path.svg
```

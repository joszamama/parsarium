# svglib — SVG / Python

- **Pinned release:** `2.4.0`
- **Upstream:** [source repository](<https://github.com/deeplook/svglib>) · [PyPI](<https://pypi.org/project/svglib/>)
- **License:** LGPL-3.0-or-later
- **Parsed scope:** SVG-to-ReportLab drawing geometry
- **Underlying family:** svglib SVG-to-ReportLab converter
- **Local input API:** `svglib.svglib.svg2rlg(local_svg_path)`
- **Documentation:** [API reference](<https://pypi.org/project/svglib/2.4.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size_points": [
    1.5,
    0.75
  ],
  "groups": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/svglib/README.md)

```sh
python3 parsarium.py build svg python svglib
python3 parsarium.py run svg python svglib controls/svg/red-green.svg
```

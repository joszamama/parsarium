# svgutils — SVG / Python

- **Pinned release:** `0.3.4`
- **License:** MIT
- **Parsed scope:** SVG element tree and dimensions
- **Underlying family:** svgutils lxml SVG tree wrapper
- **Local input API:** `svgutils.transform.fromfile(local_svg_path)`
- **Documentation:** [API reference](<https://svgutils.readthedocs.io/en/latest/transform.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    "2",
    "1"
  ],
  "elements": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/svgutils/README.md)

```sh
python3 parsarium.py build svg python svgutils
python3 parsarium.py run svg python svgutils controls/svg/red-green.svg
```

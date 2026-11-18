# svgelements — SVG / Python

- **Pinned release:** `1.9.6`
- **Upstream:** [source repository](<https://github.com/meerk40t/svgelements>) · [PyPI](<https://pypi.org/project/svgelements/>)
- **License:** MIT
- **Parsed scope:** SVG geometry elements and dimensions
- **Underlying family:** svgelements Python SVG geometry parser
- **Local input API:** `svgelements.SVG.parse(local_svg_path)`
- **Documentation:** [API reference](<https://github.com/meerk40t/svgelements>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "rectangles": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/svgelements/README.md)

```sh
python3 parsarium.py build svg python svgelements
python3 parsarium.py run svg python svgelements controls/svg/red-green.svg
```

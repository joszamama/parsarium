# Wand — SVG / Python

- **Pinned release:** `0.7.2`
- **Upstream:** [source repository](<https://github.com/emcconville/wand>) · [PyPI](<https://pypi.org/project/Wand/>)
- **License:** MIT
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** ImageMagick SVG coder through Wand
- **Local input API:** `wand.image.Image(filename=local_svg_path)`
- **Documentation:** [API reference](<https://docs.wand-py.org/en/latest/guide/read.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "red": [
    255,
    0,
    0,
    255
  ],
  "green": [
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/wand/README.md)

```sh
python3 parsarium.py build svg python wand
python3 parsarium.py run svg python wand controls/svg/red-green.svg
```

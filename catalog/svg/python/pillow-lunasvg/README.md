# pillow-lunasvg — SVG / Python

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** LunaSVG/plutovg through Pillow plugin
- **Local input API:** `import pillow_lunasvg; PIL.Image.open(local_svg_path)`
- **Documentation:** [API reference](<https://pypi.org/project/pillow-lunasvg/0.1.1/>)
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

[Docker harness and verification receipt](../../../../projects/svg/python/pillow_lunasvg/README.md)

```sh
python3 parsarium.py build svg python pillow_lunasvg
python3 parsarium.py run svg python pillow_lunasvg controls/svg/red-green.svg
```

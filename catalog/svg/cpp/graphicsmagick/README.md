# graphicsmagick — SVG / C++

- **Pinned release:** `1.3.49`
- **License:** MIT
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** GraphicsMagick SVG-to-MVG coder with libxml2
- **Local input API:** `Magick::Image(local filename); pixelColor(0,0), pixelColor(1,0)`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/formats.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

The pinned GraphicsMagick SVG coder links system libxml2 and translates SVG to MVG. It is a separate package and SVG implementation; system libxml2 is a shared XML dependency.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/cpp/graphicsmagick/README.md)

```sh
python3 parsarium.py build svg cpp graphicsmagick
python3 parsarium.py run svg cpp graphicsmagick controls/svg/red-green.svg
```

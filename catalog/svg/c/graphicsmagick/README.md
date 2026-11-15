# graphicsmagick — SVG / C

- **Pinned release:** `1.3.49`
- **License:** MIT
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** GraphicsMagick SVG-to-MVG coder with libxml2
- **Local input API:** `MagickReadImage(wand, local filename); MagickGetImagePixels`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/formats.html>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

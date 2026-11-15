# imagemagick — SVG / C

- **Pinned release:** `7.1.2-35`
- **License:** ImageMagick
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** ImageMagick internal MSVG renderer with libxml2
- **Local input API:** `MagickReadImage(wand, "MSVG:" + local filename); MagickExportImagePixels`
- **Documentation:** [API reference](<https://imagemagick.org/formats/>)
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

The adapter forces ImageMagick's documented MSVG format, selecting its internal SVG renderer. The pinned SVG coder module links system libxml2; this path does not use librsvg or the external Inkscape delegate.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

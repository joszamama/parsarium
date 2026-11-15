# graphicsmagick — ASCII PNM / C++

- **Pinned release:** `1.3.49`
- **License:** MIT
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** GraphicsMagick PNM coder
- **Local input API:** `MagickReadImage(MagickWand*, const char*); MagickGetImagePixels(...)`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/wand/magick_wand.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

GraphicsMagick MagickWand parsed P3; primary SourceForge project lacks a comparable GitHub star metric.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

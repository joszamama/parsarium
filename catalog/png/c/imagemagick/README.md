# imagemagick — PNG / C

- **Pinned release:** `7.1.2-35`
- **License:** ImageMagick
- **Parsed scope:** pixels
- **Underlying family:** ImageMagick PNG coder (libpng-backed)
- **Local input API:** `MagickReadImage(MagickWand*, const char*); MagickExportImagePixels(...)`
- **Documentation:** [API reference](<https://imagemagick.org/magick-wand/>)
- **Catalog evidence:** [parser record](../../../../data/c/png/parsers.json) · [control verification](../../../../data/c/png/verification.json) · [within-ecosystem ranking](../../../../data/c/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

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

MagickWand is the C API; the PNG coder delegates to libpng.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

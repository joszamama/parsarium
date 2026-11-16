# graphicsmagick — PNG / C

- **Pinned release:** `1.3.49`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** GraphicsMagick PNG coder (libpng-backed)
- **Local input API:** `MagickReadImage(MagickWand*, const char*); MagickGetImagePixels(...)`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/wand/magick_wand.html>)
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

GraphicsMagick Wand C package path, distinct from ImageMagick but using libpng for PNG. SourceForge upstream has no comparable GitHub primary-repository stars.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/graphicsmagick/README.md)

```sh
python3 parsarium.py build png c graphicsmagick
python3 parsarium.py run png c graphicsmagick controls/png/red-green.png
```

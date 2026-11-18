# imagemagick — PNG / C++

- **Pinned release:** `7.1.2-35`
- **Upstream:** [source repository](<https://github.com/ImageMagick/ImageMagick>) · [Debian](<https://tracker.debian.org/pkg/imagemagick>)
- **License:** ImageMagick
- **Parsed scope:** pixels
- **Underlying family:** ImageMagick PNG coder (libpng-backed)
- **Local input API:** `MagickReadImage(MagickWand*, const char*); MagickExportImagePixels(...)`
- **Documentation:** [API reference](<https://imagemagick.org/magick-wand/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
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

MagickWand is the C API; the PNG coder delegates to libpng. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/imagemagick/README.md)

```sh
python3 parsarium.py build png cpp imagemagick
python3 parsarium.py run png cpp imagemagick controls/png/red-green.png
```

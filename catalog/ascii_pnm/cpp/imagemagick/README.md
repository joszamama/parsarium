# imagemagick — ASCII PNM / C++

- **Pinned release:** `7.1.2-35`
- **Upstream:** [source repository](<https://github.com/ImageMagick/ImageMagick>) · [Debian](<https://tracker.debian.org/pkg/imagemagick>)
- **License:** ImageMagick
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** ImageMagick PNM coder
- **Local input API:** `MagickReadImage(MagickWand*, const char*); MagickExportImagePixels(...)`
- **Documentation:** [API reference](<https://imagemagick.org/magick-wand/>)
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

ImageMagick MagickWand parses ASCII P3 as a PNM image; repository stars reflect many formats.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/cpp/imagemagick/README.md)

```sh
python3 parsarium.py build ascii_pnm cpp imagemagick
python3 parsarium.py run ascii_pnm cpp imagemagick controls/ascii_pnm/red-green.ppm
```

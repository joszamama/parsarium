# pecl/imagick — ASCII PNM / PHP

- **Pinned release:** `3.8.1`
- **License:** PHP-3.01
- **Parsed scope:** decoded dimensions and RGB pixels
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Imagick::readImage(local P3 path); getImageWidth/getImageHeight/getImagePixelColor`
- **Documentation:** [API reference](<https://www.php.net/manual/en/imagick.readimage.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

PECL Imagick is an open-source extension built from a SHA-256-pinned release; it delegates ASCII P3 decoding to installed ImageMagick, not to bundled PHP GD.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/pecl_imagick/README.md)

```sh
python3 parsarium.py build ascii_pnm php pecl_imagick
python3 parsarium.py run ascii_pnm php pecl_imagick controls/ascii_pnm/red-green.ppm
```

# calcinai/php-imagick — ASCII PNM / PHP

- **Pinned release:** `v0.1.2`
- **License:** MIT
- **Parsed scope:** decoded P6 dimensions and RGB pixels
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Imagick(local P3 file)->getImageBlob(); observe decoded P6 dimensions and RGB pixels`
- **Documentation:** [API reference](<https://github.com/calcinai/php-imagick/blob/001530b19560b9862ffe78c3ae29ad5dc2549e6d/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "maxval": 255,
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

This Composer polyfill invokes the installed ImageMagick CLI to decode ASCII P3 and emits P6 pixel bytes; it is not an independent decoder engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/calcinai_php_imagick/README.md)

```sh
python3 parsarium.py build ascii_pnm php calcinai_php_imagick
python3 parsarium.py run ascii_pnm php calcinai_php_imagick controls/ascii_pnm/red-green.ppm
```

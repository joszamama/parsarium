# jcupitt/vips — ASCII PNM / PHP

- **Pinned release:** `v2.6.1`
- **Upstream:** [source repository](<https://github.com/libvips/php-vips>) · [Packagist](<https://packagist.org/packages/jcupitt/vips>)
- **License:** MIT
- **Parsed scope:** decoded dimensions and RGB pixels
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `Image::newFromFile(local P3 file); width/height and getpoint pixels`
- **Documentation:** [API reference](<https://github.com/libvips/php-vips/blob/6dbba1bb3a4ba1e39edb71016a2aa6da5bff32ee/README.md>)
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

This package path delegates ASCII P3 decoding to libvips through the PHP Vips binding. It is not an independent decoder engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/jcupitt_vips/README.md)

```sh
python3 parsarium.py build ascii_pnm php jcupitt_vips
python3 parsarium.py run ascii_pnm php jcupitt_vips controls/ascii_pnm/red-green.ppm
```

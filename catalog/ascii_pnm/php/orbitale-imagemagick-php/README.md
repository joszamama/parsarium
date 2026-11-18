# orbitale/imagemagick-php — ASCII PNM / PHP

- **Pinned release:** `v3.3.5`
- **Upstream:** [source repository](<https://github.com/Orbitale/ImageMagickPHP>) · [Packagist](<https://packagist.org/packages/orbitale/imagemagick-php>)
- **License:** MIT
- **Parsed scope:** identified PPM type and dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Command::identify(local P3 file)->run()->getOutput(); observe PPM type and dimensions`
- **Documentation:** [API reference](<https://github.com/Orbitale/ImageMagickPHP/blob/dd484b6c6e2741132a6f1bbe70ba940f0834d202/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "PPM"
}
```

This Composer command wrapper invokes the installed ImageMagick CLI to identify ASCII P3; it is not an independent decoder engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/orbitale_imagemagick_php/README.md)

```sh
python3 parsarium.py build ascii_pnm php orbitale_imagemagick_php
python3 parsarium.py run ascii_pnm php orbitale_imagemagick_php controls/ascii_pnm/red-green.ppm
```

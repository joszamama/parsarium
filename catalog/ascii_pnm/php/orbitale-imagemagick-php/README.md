# orbitale/imagemagick-php — ASCII PNM / PHP

- **Pinned release:** `v3.3.5`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# locomotivemtl/charcoal-image — ASCII PNM / PHP

- **Pinned release:** `v0.4.3.4`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Charcoal\Image\Imagick\ImagickImage::open(local P3 file); width/height`
- **Documentation:** [API reference](<https://github.com/locomotivemtl/charcoal-image/blob/d94c2b9809c12fe63bac05702db6124537d843c5/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This Composer image wrapper delegates ASCII P3 decoding to PECL Imagick and installed ImageMagick; it is not an independent decoder engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

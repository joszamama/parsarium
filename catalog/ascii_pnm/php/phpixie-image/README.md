# phpixie/image — ASCII PNM / PHP

- **Pinned release:** `3.3`
- **License:** BSD-3-Clause
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `PHPixie\Image::read(local P3 file, imagick driver); width/height`
- **Documentation:** [API reference](<https://github.com/PHPixie/Image/blob/a75f6cb484c8b8a5f26c4e2772d81fdff71b3265/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

PHPixie Image delegates ASCII P3 decoding to the separately built PECL Imagick extension and ImageMagick; it is not an independent decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

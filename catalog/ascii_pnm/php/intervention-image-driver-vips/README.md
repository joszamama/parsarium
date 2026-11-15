# intervention/image-driver-vips — ASCII PNM / PHP

- **Pinned release:** `4.2.0`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `Vips\Driver::decodeImage(local P3 file); width/height`
- **Documentation:** [API reference](<https://github.com/Intervention/image-driver-vips/blob/2aca734a68c447aed1304d8b2121b223d2790e00/src/Driver.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This package path delegates ASCII P3 decoding to libvips through the PHP Vips binding. It is not an independent decoder engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

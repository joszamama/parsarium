# osiemsiedem/intervention-image-vips-driver — ASCII PNM / PHP

- **Pinned release:** `v0.11.0`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `Vips\Decoder::initFromPath(local P3 file); width/height`
- **Documentation:** [API reference](<https://github.com/osiemsiedem/intervention-image-vips-driver/blob/3068585d60277674f9ebfc73e5577db86ab28e4a/src/Decoder.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This package path delegates ASCII P3 decoding to libvips through the PHP Vips binding. It is not an independent decoder engine. This older package is marked abandoned by Packagist.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

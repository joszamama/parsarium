# rokka/imagine-vips — ASCII PNM / PHP

- **Pinned release:** `0.42.0`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `Imagine\Vips\Imagine::open(local P3 file); getSize`
- **Documentation:** [API reference](<https://github.com/rokka-io/imagine-vips/blob/b6382de7104d96f2f7df277e403927fab85a4b41/README.md>)
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

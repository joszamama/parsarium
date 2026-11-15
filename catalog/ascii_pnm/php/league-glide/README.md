# league/glide — ASCII PNM / PHP

- **Pinned release:** `4.2.0`
- **License:** MIT
- **Parsed scope:** converted PNG dimensions and MIME
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `ServerFactory::create(local source directory, Imagick driver)->makeImage(P3 filename, PNG output); inspect converted image dimensions`
- **Documentation:** [API reference](<https://github.com/thephpleague/glide/blob/704e51e1bf4af99a9efd6d3083d7fab41718e8f1/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "mime": "image/png"
}
```

Glide reads local P3 bytes and delegates decoding to Intervention Image with the separately built PECL Imagick extension and ImageMagick; it is not an independent decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

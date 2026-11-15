# intervention/image-laravel — ASCII PNM / PHP

- **Pinned release:** `4.1.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Laravel Image facade::decodePath(local P3 file) using the package service provider and Imagick driver; width/height`
- **Documentation:** [API reference](<https://github.com/Intervention/image-laravel/blob/8a8bd2c7bb4a9aa2b046ff066fd1cd44b1de0da2/src/Facades/Image.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The Laravel integration package registers a facade that delegates ASCII P3 decoding to Intervention Image and PECL Imagick/ImageMagick. The adapter supplies a minimal pinned Illuminate container, config repository, and config helper.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

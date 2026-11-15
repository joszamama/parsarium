# phpthumb/phpthumb — ASCII PNM / PHP

- **Pinned release:** `2.5.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `PHPThumb\Imagick(local P3 file)->getCurrentDimensions()`
- **Documentation:** [API reference](<https://github.com/PHPThumb/PHPThumb/blob/b76d5bd7b53a69ac0c9572802b06c7071479cf04/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This Composer wrapper delegates ASCII P3 decoding to PECL Imagick and installed ImageMagick; it is not an independent decoder engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

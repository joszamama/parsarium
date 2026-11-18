# imagine/imagine — ASCII PNM / PHP

- **Pinned release:** `1.5.4`
- **Upstream:** [source repository](<https://github.com/php-imagine/Imagine>) · [Packagist](<https://packagist.org/packages/imagine/imagine>)
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Imagine\Imagick\Imagine::open(local P3 file); getSize`
- **Documentation:** [API reference](<https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Imagick/Imagine.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This package path delegates ASCII P3 decoding to the separately built PECL Imagick extension and ImageMagick; it is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/imagine/README.md)

```sh
python3 parsarium.py build ascii_pnm php imagine
python3 parsarium.py run ascii_pnm php imagine controls/ascii_pnm/red-green.ppm
```

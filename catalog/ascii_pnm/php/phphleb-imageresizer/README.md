# phphleb/imageresizer — ASCII PNM / PHP

- **Pinned release:** `v2.0.8`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `SimpleImage::load(local P3 file) with Imagick processor; getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/phphleb/imageresizer/blob/b785b6b9c9089e836c669136d70230988ef91d07/readme.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The package uses PECL Imagick and installed ImageMagick to decode P3. The README lists common formats but not PNM; this pinned release accepts the valid P3 control through its documented local-path API.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/phphleb_imageresizer/README.md)

```sh
python3 parsarium.py build ascii_pnm php phphleb_imageresizer
python3 parsarium.py run ascii_pnm php phphleb_imageresizer controls/ascii_pnm/red-green.ppm
```

# tpmanc/yii2-imagick — ASCII PNM / PHP

- **Pinned release:** `1.3.2`
- **License:** BSD-3-Clause
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `tpmanc\imagick\Imagick::open(local P3 file); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/tpmanc/yii2-imagick/blob/be5f3c1dc1b1f18acde1f4672bf6d4dc77f2fd1a/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The package delegates ASCII P3 decoding to PECL Imagick and ImageMagick.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/tpmanc_yii2_imagick/README.md)

```sh
python3 parsarium.py build ascii_pnm php tpmanc_yii2_imagick
python3 parsarium.py run ascii_pnm php tpmanc_yii2_imagick controls/ascii_pnm/red-green.ppm
```

# horde/image — ASCII PNM / PHP

- **Pinned release:** `v3.0.0`
- **License:** LGPL-2.1-only
- **Parsed scope:** decoded image dimensions
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `Horde\Image\Driver\ImagickDriver::loadFile(local P3 file); size()`
- **Documentation:** [API reference](<https://github.com/horde/Image/blob/a7686307adba2f25f32be6b219d51742fb338ba6/doc/USAGE.md>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/horde_image/README.md)

```sh
python3 parsarium.py build ascii_pnm php horde_image
python3 parsarium.py run ascii_pnm php horde_image controls/ascii_pnm/red-green.ppm
```

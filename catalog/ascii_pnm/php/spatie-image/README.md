# spatie/image — ASCII PNM / PHP

- **Pinned release:** `3.9.10`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `Image::useImageDriver(Vips)->loadFile(local P3 file); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/spatie/image/blob/de071f9aceaeed977401d6983a8bbe0c21b411dd/src/Image.php>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/spatie_image/README.md)

```sh
python3 parsarium.py build ascii_pnm php spatie_image
python3 parsarium.py run ascii_pnm php spatie_image controls/ascii_pnm/red-green.ppm
```

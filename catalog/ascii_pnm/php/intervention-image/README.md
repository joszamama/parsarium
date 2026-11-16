# intervention/image — ASCII PNM / PHP

- **Pinned release:** `4.4.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PPM/PNM decoder
- **Local input API:** `ImageManager(VipsDriver)->decodePath(local P3 file); width/height`
- **Documentation:** [API reference](<https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/src/ImageManager.php>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/intervention_image/README.md)

```sh
python3 parsarium.py build ascii_pnm php intervention_image
python3 parsarium.py run ascii_pnm php intervention_image controls/ascii_pnm/red-green.ppm
```

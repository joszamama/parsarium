# spatie/image — PNG / PHP

- **Pinned release:** `3.9.10`
- **Upstream:** [source repository](<https://github.com/spatie/image>) · [Packagist](<https://packagist.org/packages/spatie/image>)
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Image::useImageDriver(Gd)->loadFile(local PNG path); getWidth/getHeight`
- **Documentation:** [API reference](<https://spatie.be/docs/image/v3/usage/basic-usage>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The adapter selects Spatie’s GD driver, which delegates PNG decoding to PHP GD.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/spatie_image/README.md)

```sh
python3 parsarium.py build png php spatie_image
python3 parsarium.py run png php spatie_image controls/png/red-green.png
```

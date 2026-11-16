# contao/image — PNG / PHP

- **Pinned release:** `1.2.4`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** PNG decoded and resized to 1×1
- **Underlying family:** Imagine / PHP GD PNG decoder
- **Local input API:** `Contao\Image\Image(local PNG path, Imagine GD); Resizer::resize`
- **Documentation:** [API reference](<https://github.com/contao/image/blob/06cafbcf787276b0a1639b44c89439dde14ca151/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 1,
  "height": 1,
  "type": 3
}
```

Contao uses Imagine GD to decode and resize the PNG; its dimension path also calls bundled getimagesize.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/contao_image/README.md)

```sh
python3 parsarium.py build png php contao_image
python3 parsarium.py run png php contao_image controls/png/red-green.png
```

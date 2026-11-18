# gumlet/php-image-resize — PNG / PHP

- **Pinned release:** `3.0.1`
- **Upstream:** [source repository](<https://github.com/gumlet/php-image-resize>) · [Packagist](<https://packagist.org/packages/gumlet/php-image-resize>)
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `ImageResize(local PNG path); getSourceWidth/getSourceHeight`
- **Documentation:** [API reference](<https://github.com/gumlet/php-image-resize/blob/cd01c9e8aa2382211d760c825799c8102987a8c2/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The package loads the local PNG through PHP GD.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/gumlet_php_image_resize/README.md)

```sh
python3 parsarium.py build png php gumlet_php_image_resize
python3 parsarium.py run png php gumlet_php_image_resize controls/png/red-green.png
```

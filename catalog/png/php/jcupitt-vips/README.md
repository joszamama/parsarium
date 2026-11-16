# jcupitt/vips — PNG / PHP

- **Pinned release:** `v2.6.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** libvips PNG decoder
- **Local input API:** `Image::newFromFile(local PNG path); width/height fields`
- **Documentation:** [API reference](<https://github.com/libvips/php-vips/blob/6dbba1bb3a4ba1e39edb71016a2aa6da5bff32ee/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

PHP FFI binding delegates PNG decoding to installed libvips 8.18.7, a separate family from PHP GD.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/jcupitt_vips/README.md)

```sh
python3 parsarium.py build png php jcupitt_vips
python3 parsarium.py run png php jcupitt_vips controls/png/red-green.png
```

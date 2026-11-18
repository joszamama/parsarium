# marc1706/fast-image-size — PNG / PHP

- **Pinned release:** `v1.3.1`
- **Upstream:** [source repository](<https://github.com/marc1706/fast-image-size>) · [Packagist](<https://packagist.org/packages/marc1706/fast-image-size>)
- **License:** MIT
- **Parsed scope:** PNG dimensions and format type
- **Underlying family:** FastImageSize PNG header reader
- **Local input API:** `FastImageSize::getImageSize(local PNG path)`
- **Documentation:** [API reference](<https://packagist.org/packages/marc1706/fast-image-size>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": 3
}
```

Parses PNG dimensions and type from headers in PHP; it does not decode pixels.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/marc1706_fast_image_size/README.md)

```sh
python3 parsarium.py build png php marc1706_fast_image_size
python3 parsarium.py run png php marc1706_fast_image_size controls/png/red-green.png
```

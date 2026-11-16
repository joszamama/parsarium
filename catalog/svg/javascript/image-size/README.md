# image-size — SVG / JavaScript

- **Pinned release:** `2.1.0`
- **License:** MIT
- **Parsed scope:** dimensions
- **Underlying family:** image-size SVG reader
- **Local input API:** `imageSize(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/image-size>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "svg"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/image_size/README.md)

```sh
python3 parsarium.py build svg javascript image_size
python3 parsarium.py run svg javascript image_size controls/svg/red-green.svg
```

# @loaders.gl/images — PNG / JavaScript

- **Pinned release:** `4.5.4`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** loaders.gl binary-image-api
- **Local input API:** `getBinaryImageMetadata(ArrayBuffer)`
- **Documentation:** [API reference](<https://loaders.gl/docs/modules/images/api-reference/binary-image-api>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": "png"
}
```

Reads encoded PNG header fields; does not decode pixels through this API.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/loaders_gl_images/README.md)

```sh
python3 parsarium.py build png javascript loaders_gl_images
python3 parsarium.py run png javascript loaders_gl_images controls/png/red-green.png
```

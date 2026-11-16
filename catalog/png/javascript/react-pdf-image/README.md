# @react-pdf/image — PNG / JavaScript

- **Pinned release:** `3.1.2`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** png.js
- **Local input API:** `resolveImage(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@react-pdf/image>)
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

The pinned package depends on png-js@^2.0.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/react_pdf_image/README.md)

```sh
python3 parsarium.py build png javascript react_pdf_image
python3 parsarium.py run png javascript react_pdf_image controls/png/red-green.png
```

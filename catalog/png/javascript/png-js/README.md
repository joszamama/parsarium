# png-js — PNG / JavaScript

- **Pinned release:** `2.0.0`
- **License:** MIT (upstream LICENSE; npm metadata omits license)
- **Parsed scope:** pixels
- **Underlying family:** png.js
- **Local input API:** `new PNG(Buffer).decode(callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/png-js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/png_js/README.md)

```sh
python3 parsarium.py build png javascript png_js
python3 parsarium.py run png javascript png_js controls/png/red-green.png
```

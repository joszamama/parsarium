# upng-js — PNG / JavaScript

- **Pinned release:** `2.1.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** UPNG.js
- **Local input API:** `UPNG.decode(ArrayBuffer); UPNG.toRGBA8(image)`
- **Documentation:** [API reference](<https://github.com/photopea/UPNG.js/blob/master/README.md>)
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

[Docker harness and verification receipt](../../../../projects/png/javascript/upng_js/README.md)

```sh
python3 parsarium.py build png javascript upng_js
python3 parsarium.py run png javascript upng_js controls/png/red-green.png
```

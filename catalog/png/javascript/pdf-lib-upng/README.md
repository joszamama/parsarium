# @pdf-lib/upng — PNG / JavaScript

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** UPNG.js
- **Local input API:** `UPNG.decode(ArrayBuffer); UPNG.toRGBA8(image)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@pdf-lib/upng>)
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

Fork of the UPNG.js decoder also published as upng-js.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/pdf_lib_upng/README.md)

```sh
python3 parsarium.py build png javascript pdf_lib_upng
python3 parsarium.py run png javascript pdf_lib_upng controls/png/red-green.png
```

# canvas — PNG / JavaScript

- **Pinned release:** `3.2.3`
- **Upstream:** [source repository](<https://github.com/Automattic/node-canvas>) · [npm](<https://www.npmjs.com/package/canvas>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Cairo/libpng
- **Local input API:** `loadImage(Buffer); drawImage; getImageData`
- **Documentation:** [API reference](<https://github.com/Automattic/node-canvas#imagesrc>)
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

Native Canvas binding; PNG decoding is delegated to the Cairo/libpng stack.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/canvas/README.md)

```sh
python3 parsarium.py build png javascript canvas
python3 parsarium.py run png javascript canvas controls/png/red-green.png
```

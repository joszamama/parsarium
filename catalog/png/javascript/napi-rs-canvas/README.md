# @napi-rs/canvas — PNG / JavaScript

- **Pinned release:** `1.1.0`
- **Upstream:** [source repository](<https://github.com/Brooooooklyn/canvas>) · [npm](<https://www.npmjs.com/package/@napi-rs/canvas>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Skia
- **Local input API:** `loadImage(Buffer); drawImage; getImageData`
- **Documentation:** [API reference](<https://github.com/Brooooooklyn/canvas/blob/main/index.d.ts>)
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

Native Node-API binding; pinned package type declarations document Buffer input.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/napi_rs_canvas/README.md)

```sh
python3 parsarium.py build png javascript napi_rs_canvas
python3 parsarium.py run png javascript napi_rs_canvas controls/png/red-green.png
```

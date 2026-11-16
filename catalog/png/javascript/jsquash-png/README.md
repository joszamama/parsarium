# @jsquash/png — PNG / JavaScript

- **Pinned release:** `3.1.1`
- **License:** Apache-2.0
- **Parsed scope:** pixels
- **Underlying family:** Rust png crate via jSquash WASM
- **Local input API:** `init(local WASM bytes); decode(ArrayBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@jsquash/png>)
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

[Docker harness and verification receipt](../../../../projects/png/javascript/jsquash_png/README.md)

```sh
python3 parsarium.py build png javascript jsquash_png
python3 parsarium.py run png javascript jsquash_png controls/png/red-green.png
```

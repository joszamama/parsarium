# @resvg/resvg-wasm — SVG / JavaScript

- **Pinned release:** `2.6.2`
- **License:** MPL-2.0
- **Parsed scope:** pixels
- **Underlying family:** resvg
- **Local input API:** `initWasm(localWasmBytes); new Resvg(svgString).render().pixels`
- **Documentation:** [API reference](<https://unpkg.com/@resvg/resvg-wasm@2.6.2/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

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

WebAssembly distribution of the same Rust resvg engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/resvg_resvg_wasm/README.md)

```sh
python3 parsarium.py build svg javascript resvg_resvg_wasm
python3 parsarium.py run svg javascript resvg_resvg_wasm controls/svg/red-green.svg
```

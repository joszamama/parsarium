# @resvg/resvg-js — SVG / JavaScript

- **Pinned release:** `2.6.2`
- **Upstream:** [source repository](<https://github.com/thx/resvg-js>) · [npm](<https://www.npmjs.com/package/@resvg/resvg-js>)
- **License:** MPL-2.0
- **Parsed scope:** pixels
- **Underlying family:** resvg
- **Local input API:** `new Resvg(svgString).render().pixels`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@resvg/resvg-js>)
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

Native binding around Rust resvg.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/resvg_resvg_js/README.md)

```sh
python3 parsarium.py build svg javascript resvg_resvg_js
python3 parsarium.py run svg javascript resvg_resvg_js controls/svg/red-green.svg
```

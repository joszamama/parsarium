# svg2img — SVG / JavaScript

- **Pinned release:** `1.0.0-beta.2`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** resvg
- **Local input API:** `svg2img(svgString,callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/svg2img>)
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

README states the v1 conversion backend is resvg-js.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# sharp — SVG / JavaScript

- **Pinned release:** `0.35.5`
- **License:** Apache-2.0
- **Parsed scope:** dimensions
- **Underlying family:** libvips/librsvg
- **Local input API:** `sharp(Buffer).metadata()`
- **Documentation:** [API reference](<https://sharp.pixelplumbing.com/api-input/>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "svg"
}
```

Native libvips SVG input backend.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

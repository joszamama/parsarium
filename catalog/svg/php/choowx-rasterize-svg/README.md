# choowx/rasterize-svg — SVG / PHP

- **Pinned release:** `v0.1.2`
- **License:** MIT
- **Parsed scope:** Rendered simple two-rectangle SVG to 2 × 1 PNG; sharp 0.35.5 is pinned by repository package-lock.json.
- **Underlying family:** sharp/libvips SVG renderer
- **Local input API:** `Svg::make(local SVG bytes)->toPng invokes pinned Node sharp renderer; decoded pixel result`
- **Documentation:** [API reference](<https://github.com/choowx/rasterize-svg/blob/d23fad7be783ebb15097e5abb31621223917ce9a/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

PHP package invokes a Node script requiring sharp; underlying SVG engine is sharp/libvips, not native PHP.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

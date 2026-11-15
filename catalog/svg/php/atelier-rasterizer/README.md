# atelier/rasterizer — SVG / PHP

- **Pinned release:** `v0.7.0`
- **License:** MIT
- **Parsed scope:** Rendered two-rectangle SVG to a 2 × 1 PNG using external librsvg 2.63.4.
- **Underlying family:** GNOME librsvg SVG renderer via rsvg-convert
- **Local input API:** `SvgInput::fromFile(local path), Rasterizer::rsvgConvert()->rasterize; decoded PNG dimensions and pixels`
- **Documentation:** [API reference](<https://github.com/ateliersvg/rasterizer/blob/7c9afe94dfd9a70446a1f3cda949ea4422de1bb4/README.md>)
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

PHP package is a wrapper over the pinned host rsvg-convert binary; not an independent SVG engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

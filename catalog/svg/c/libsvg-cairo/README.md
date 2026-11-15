# libsvg-cairo — SVG / C

- **Pinned release:** `0.1.6`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** libsvg-cairo adapter over libsvg parser and Cairo renderer
- **Local input API:** `svg_cairo_create; svg_cairo_parse(local filename); svg_cairo_get_size; svg_cairo_render to Cairo image surface`
- **Documentation:** [API reference](<https://cairographics.org/snapshots/libsvg-cairo-0.1.6.tar.gz>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

A distinct package input API, but SVG syntax parsing is delegated to the separately counted libsvg 0.1.4 package. Cairo supplies rasterization.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

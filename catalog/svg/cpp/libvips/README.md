# libvips — SVG / C++

- **Pinned release:** `8.18.7`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** libvips SVG loader over librsvg
- **Local input API:** `vips::VImage::svgload(local filename); getpoint(x,y)`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/ctor.Image.svgload.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
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

Installed libvips core directly links librsvg 2.63.4. libvips is a distinct package input API but shares SVG syntax interpretation with the librsvg row.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

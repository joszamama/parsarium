# libsvgtiny — SVG / C

- **Pinned release:** `0.1.8`
- **License:** MIT
- **Parsed scope:** parsed SVG dimensions, two shapes, and red/green fill colors
- **Underlying family:** NetSurf libsvgtiny SVG Tiny parser over libdom
- **Local input API:** `svgtiny_parse(local SVG file bytes, size, URL, viewport); diagram width, height, shape count and fill colors`
- **Documentation:** [API reference](<https://www.netsurf-browser.org/projects/libsvgtiny/>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "shapes": 2,
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

The same C source library serves C and C++ call sites. libsvgtiny uses the NetSurf libdom XML parser and returns parsed shapes; it does not rasterize.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

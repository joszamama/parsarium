# libsvg — SVG / C++

- **Pinned release:** `0.1.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG root dimensions
- **Underlying family:** libsvg parser with system libxml2
- **Local input API:** `svg_create; svg_parse(local filename); svg_get_size parsed SVG width and height`
- **Documentation:** [API reference](<https://cairographics.org/snapshots/libsvg-0.1.4.tar.gz>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

libsvg parses SVG without drawing. Its README says it was based on old librsvg code; the installed library is separate from current librsvg. libsvg-cairo uses this same underlying parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

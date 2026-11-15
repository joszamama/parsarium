# novasvg — SVG / C++

- **Pinned release:** `0.11.5`
- **License:** MIT
- **Parsed scope:** SVG root dimensions and two parsed rectangle elements
- **Underlying family:** NovaSVG native C++ SVG parser
- **Local input API:** `novasvg::Document::loadFromFile(local filename); width(); height(); querySelectorAll("rect")`
- **Documentation:** [API reference](<https://mohammadraziei.github.io/novasvg/index.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rectangles": 2
}
```

Header-only C++17 library with its own SVG document parser and rasterizer.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

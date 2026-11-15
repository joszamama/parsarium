# yoya/php-svg — SVG / PHP

- **Pinned release:** `v1.0.0`
- **License:** MIT
- **Parsed scope:** Typed SVG root dimensions and two parsed rectangle child nodes.
- **Underlying family:** mediashowroom PHP-SVG typed document parser
- **Local input API:** `SVG\SVGImage::fromFile(local path) parses SVG document and direct child shapes`
- **Documentation:** [API reference](<https://github.com/yoya/php-svg/blob/851e3b06b14c26acd55a5bd1165dd770353ba40f/src/SVGImage.php>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": "2",
  "height": "1",
  "rectangles": 2
}
```

Fork of older mediashowroom PHP-SVG code; shares parser lineage with mediashowroom/php-svg and meyfa/php-svg.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# gsvg — SVG / Java

- **Pinned release:** `1.2.0`
- **License:** MIT
- **Parsed scope:** Typed SVG dimensions, rectangle elements, and fill attributes
- **Underlying family:** gsvg typed SVG model (Groovy library callable from Java)
- **Local input API:** `SvgReader.parse(File).findAll(Rect.class)`
- **Documentation:** [API reference](<https://github.com/Alipsa/gsvg#readparse-an-existing-svg-file-and-change-it>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2,
  "fills": "#ff0000,#00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

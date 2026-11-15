# mober/phpsvg — SVG / PHP

- **Pinned release:** `v6.0.0`
- **License:** GPL-3.0
- **Parsed scope:** Typed SVG document wrapper over SimpleXML with two rectangle nodes observed.
- **Underlying family:** mober phpsvg SimpleXML SVG document parser
- **Local input API:** `new SVGDocument(local SVG path) parses width, height, and rectangle nodes`
- **Documentation:** [API reference](<https://github.com/m-ober/phpsvg/blob/96d7c06218186a4395fc26074ed3a6b3213a5d9d/src/SVGDocument.php>)
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

Fork of older mewebstudio/phpsvg, not meyfa/php-svg. Uses SimpleXML for XML syntax.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

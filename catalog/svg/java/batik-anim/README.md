# batik-anim — SVG / Java

- **Pinned release:** `1.20`
- **License:** Apache-2.0
- **Parsed scope:** SVG DOM dimensions and rectangle elements
- **Underlying family:** Apache Batik SVG DOM
- **Local input API:** `SAXSVGDocumentFactory.createDocument(String URI, InputStream)`
- **Documentation:** [API reference](<https://xmlgraphics.apache.org/batik/using/dom-api.html>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

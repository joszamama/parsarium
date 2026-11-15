# echosvg-swing — SVG / Java

- **Pinned release:** `2.5`
- **License:** Apache-2.0
- **Parsed scope:** SVG DOM dimensions and rectangle elements
- **Underlying family:** EchoSVG SVG DOM and renderer via Swing (Apache Batik fork)
- **Local input API:** `JSVGCanvas.setURI(local file URI); SVGDocumentLoaderListener; getSVGDocument()`
- **Documentation:** [API reference](<https://github.com/css4j/echosvg/blob/master/echosvg-swing/src/main/java/io/sf/carte/echosvg/swing/JSVGCanvas.java>)
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

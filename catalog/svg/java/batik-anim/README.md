# batik-anim — SVG / Java

- **Pinned release:** `1.20`
- **Upstream:** [source repository](<https://github.com/apache/xmlgraphics-batik>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.xmlgraphics/batik-anim>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/batik_anim/README.md)

```sh
python3 parsarium.py build svg java batik_anim
python3 parsarium.py run svg java batik_anim controls/svg/red-green.svg
```

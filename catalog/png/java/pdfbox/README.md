# pdfbox — PNG / Java

- **Pinned release:** `3.0.8`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/org.apache.pdfbox/pdfbox>)
- **License:** Apache-2.0
- **Parsed scope:** PNG dimensions
- **Underlying family:** Apache PDFBox image embedding path
- **Local input API:** `PDImageXObject.createFromFileByContent(File,PDDocument).getWidth/getHeight`
- **Documentation:** [API reference](<https://javadoc.io/static/org.apache.pdfbox/pdfbox/3.0.8/org/apache/pdfbox/pdmodel/graphics/image/PDImageXObject.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/pdfbox/README.md)

```sh
python3 parsarium.py build png java pdfbox
python3 parsarium.py run png java pdfbox controls/png/red-green.png
```

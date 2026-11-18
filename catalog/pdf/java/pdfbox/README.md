# pdfbox — PDF / Java

- **Pinned release:** `3.0.8`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/org.apache.pdfbox/pdfbox>)
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** Apache PDFBox
- **Local input API:** `Loader.loadPDF(File).getNumberOfPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/org.apache.pdfbox/pdfbox/3.0.8/org/apache/pdfbox/Loader.html>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/pdfbox/README.md)

```sh
python3 parsarium.py build pdf java pdfbox
python3 parsarium.py run pdf java pdfbox controls/pdf/one-page.pdf
```

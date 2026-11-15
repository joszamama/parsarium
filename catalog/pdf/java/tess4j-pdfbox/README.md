# tess4j-pdfbox — PDF / Java

- **Pinned release:** `5.20.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** Tess4J PDF utility over PDFBox
- **Local input API:** `PdfBoxUtilities.getPdfPageCount(File)`
- **Documentation:** [API reference](<https://github.com/nguyenq/tess4j/blob/master/src/main/java/net/sourceforge/tess4j/util/PdfBoxUtilities.java>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

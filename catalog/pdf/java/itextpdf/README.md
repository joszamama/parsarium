# itextpdf — PDF / Java

- **Pinned release:** `5.5.13`
- **License:** AGPL-3.0
- **Parsed scope:** PDF page count
- **Underlying family:** iText 5 PDF reader
- **Local input API:** `new PdfReader(String localPath).getNumberOfPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/com.itextpdf/itextpdf/5.5.13/com/itextpdf/text/pdf/PdfReader.html>)
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

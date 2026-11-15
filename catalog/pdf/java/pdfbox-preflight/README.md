# pdfbox-preflight — PDF / Java

- **Pinned release:** `3.0.8`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** Apache PDFBox Preflight wrapper
- **Local input API:** `new PreflightParser(File).parse().getNumberOfPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/org.apache.pdfbox/preflight/3.0.8/org/apache/pdfbox/preflight/parser/PreflightParser.html>)
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

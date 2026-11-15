# pdfjet — PDF / Java

- **Pinned release:** `9.1.7`
- **License:** MIT AND OFL-1.1
- **Parsed scope:** PDF page count
- **Underlying family:** PDFjet reader
- **Local input API:** `new PDF().read(InputStream) and PDFobj /Pages /Count`
- **Documentation:** [API reference](<https://github.com/edragoev1/pdfjet>)
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

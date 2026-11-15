# pdfclown — PDF / Java

- **Pinned release:** `0.1.2-Beta`
- **License:** LGPL-3.0
- **Parsed scope:** PDF page count
- **Underlying family:** PDF Clown parser
- **Local input API:** `new org.pdfclown.files.File(String localPath).getDocument().getPages().size()`
- **Documentation:** [API reference](<https://pdfclown.org/overview/features/>)
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

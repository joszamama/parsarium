# pdf-parse — PDF / JavaScript

- **Pinned release:** `2.4.5`
- **License:** Apache-2.0
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `new PDFParse({data:Buffer}).getText()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf-parse>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Direct or transitive PDF.js use, fork, or redistribution; package count does not imply an independent parser engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

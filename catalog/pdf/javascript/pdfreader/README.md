# pdfreader — PDF / JavaScript

- **Pinned release:** `3.0.8`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `new PdfReader().parseBuffer(Buffer, callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdfreader>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Depends on pdf2json, a PDF.js-derived parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# ottosmops/pdftotext — PDF / PHP

- **Pinned release:** `2.0.1`
- **License:** MIT
- **Parsed scope:** Embedded Parsarium text extracted from PDF
- **Underlying family:** Poppler pdftotext PDF parser
- **Local input API:** `Extract::pdf(local PDF path)->text(); extracted text`
- **Documentation:** [API reference](<https://github.com/ottosmops/pdftotext/blob/ab349a44a051673c40d3d690da1e4878afb03339/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

PHP wrapper invokes local Poppler pdftotext 26.11.0; shared backend with spatie/pdf-to-text.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

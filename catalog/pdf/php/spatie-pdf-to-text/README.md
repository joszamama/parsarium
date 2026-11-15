# spatie/pdf-to-text — PDF / PHP

- **Pinned release:** `1.55.0`
- **License:** MIT
- **Parsed scope:** Embedded Parsarium text extracted from PDF
- **Underlying family:** Poppler pdftotext PDF parser
- **Local input API:** `Pdf::getText(local PDF path); extracted text`
- **Documentation:** [API reference](<https://github.com/spatie/pdf-to-text/blob/c5c6c7fa8aaa34de7eb6cde42b45aec480c8afb6/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

PHP wrapper invokes local pdftotext 26.11.0; shared native backend is recorded.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

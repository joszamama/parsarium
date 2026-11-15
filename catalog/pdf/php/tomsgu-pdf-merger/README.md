# tomsgu/pdf-merger — PDF / PHP

- **Pinned release:** `v0.5.1`
- **License:** MIT
- **Parsed scope:** One imported page object in emitted PDF
- **Underlying family:** FPDI native PHP PDF object reader
- **Local input API:** `PdfCollection::addPdf(local PDF path), PdfMerger::merge(..., MODE_STRING); one imported PDF page object`
- **Documentation:** [API reference](<https://github.com/Tomsgu/PDFMerger/blob/4093d45a9c4bcbc1c986a513b07b2736d64d253f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pdf_header": true,
  "page_objects": 1
}
```

Wrapper delegates page import to pinned FPDI 2.6.10 and uses pinned FPDF 1.9.0 as rendering companion.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

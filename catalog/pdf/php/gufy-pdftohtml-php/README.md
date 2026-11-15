# gufy/pdftohtml-php — PDF / PHP

- **Pinned release:** `v2.0.8`
- **License:** MIT
- **Parsed scope:** One PDF page and embedded Parsarium text
- **Underlying family:** Poppler pdfinfo and pdftohtml PDF parsers
- **Local input API:** `Pdf(local PDF path)->getPages(), html(); parsed page count and extracted text`
- **Documentation:** [API reference](<https://github.com/mgufrone/pdf-to-html/blob/4b0c2c60d48b8e3e08394a3f130606408e7f7d2e/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "text": "Parsarium"
}
```

PHP wrapper invokes local Poppler pdfinfo/pdftohtml 26.11.0; the release is abandoned upstream but pinned and replays on the valid control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

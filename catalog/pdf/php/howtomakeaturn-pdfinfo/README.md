# howtomakeaturn/pdfinfo — PDF / PHP

- **Pinned release:** `1.1.6`
- **License:** MIT
- **Parsed scope:** One PDF page and document title
- **Underlying family:** Poppler pdfinfo PDF parser
- **Local input API:** `PDFInfo(local PDF path); parsed pages and title metadata`
- **Documentation:** [API reference](<https://github.com/howtomakeaturn/pdfinfo/blob/564542360f4052a45905e1be80aee6f8d843e1ae/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

PHP wrapper invokes local Poppler pdfinfo 26.11.0 and parses its metadata output.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/howtomakeaturn_pdfinfo/README.md)

```sh
python3 parsarium.py build pdf php howtomakeaturn_pdfinfo
python3 parsarium.py run pdf php howtomakeaturn_pdfinfo controls/pdf/one-page.pdf
```

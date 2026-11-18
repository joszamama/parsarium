# jurosh/pdf-merge — PDF / PHP

- **Pinned release:** `2.1.0`
- **Upstream:** [source repository](<https://github.com/jurosh/php-pdf-merge>) · [Packagist](<https://packagist.org/packages/jurosh/pdf-merge>)
- **License:** Apache-2.0
- **Parsed scope:** One imported page object in emitted PDF
- **Underlying family:** FPDI native PHP PDF object reader
- **Local input API:** `PDFMerger::addPDF(local PDF path), merge(string); one imported PDF page object`
- **Documentation:** [API reference](<https://github.com/jurosh/php-pdf-merge/blob/89ba3446c9f38c573e3b8bf577d2f22993494130/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pdf_header": true,
  "page_objects": 1
}
```

Wrapper delegates page import to pinned FPDI 2.6.10. Composer metadata says MIT, but the pinned LICENSE file and README specify Apache-2.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/jurosh_pdf_merge/README.md)

```sh
python3 parsarium.py build pdf php jurosh_pdf_merge
python3 parsarium.py run pdf php jurosh_pdf_merge controls/pdf/one-page.pdf
```

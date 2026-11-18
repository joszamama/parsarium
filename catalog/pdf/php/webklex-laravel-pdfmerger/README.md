# webklex/laravel-pdfmerger — PDF / PHP

- **Pinned release:** `1.3.2`
- **Upstream:** [source repository](<https://github.com/Webklex/laravel-pdfmerger>) · [Packagist](<https://packagist.org/packages/webklex/laravel-pdfmerger>)
- **License:** MIT
- **Parsed scope:** One imported page object in emitted PDF
- **Underlying family:** FPDI native PHP PDF object reader
- **Local input API:** `PDFMerger::addPDF(local PDF path, page 1), merge(), output(); one imported PDF page object`
- **Documentation:** [API reference](<https://github.com/Webklex/laravel-pdfmerger/blob/de88152c793fb190631a050688478f4a18bbac22/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pdf_header": true,
  "page_objects": 1
}
```

Laravel-oriented wrapper delegates page import to pinned FPDI 2.6.10; illuminate/filesystem 13.42.0 is an explicit companion dependency.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/webklex_laravel_pdfmerger/README.md)

```sh
python3 parsarium.py build pdf php webklex_laravel_pdfmerger
python3 parsarium.py run pdf php webklex_laravel_pdfmerger controls/pdf/one-page.pdf
```

# asika/pdf2text — PDF / PHP

- **Pinned release:** `1.0.6`
- **License:** MIT
- **Parsed scope:** Embedded Parsarium text extracted from PDF
- **Underlying family:** SilverStripe-derived native PHP PDF text parser
- **Local input API:** `Pdf2text::decode(local PDF path); extracted text`
- **Documentation:** [API reference](<https://github.com/asika32764/php-pdf-2-text/blob/7e328221418ee237b60aee291f416633469162f7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Composer adaptation of Darren Inwood/SilverStripe PDF-to-text reader; separate package source and shared lineage noted.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/asika_pdf2text/README.md)

```sh
python3 parsarium.py build pdf php asika_pdf2text
python3 parsarium.py run pdf php asika_pdf2text controls/pdf/one-page.pdf
```

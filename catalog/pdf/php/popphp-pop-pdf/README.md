# popphp/pop-pdf — PDF / PHP

- **Pinned release:** `6.2.2`
- **License:** BSD-3-Clause
- **Parsed scope:** Embedded Parsarium text extracted from PDF
- **Underlying family:** Pop PDF native PHP parser
- **Local input API:** `Pdf::extractTextFromFile(local PDF path); extracted text`
- **Documentation:** [API reference](<https://github.com/popphp/pop-pdf/blob/c508ff26aa383f09b44d1c58ea9e3f3bffd9af2f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Own PDF object, content and text parser implementation; dependencies are pinned in its isolated Composer lock.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/popphp_pop_pdf/README.md)

```sh
python3 parsarium.py build pdf php popphp_pop_pdf
python3 parsarium.py run pdf php popphp_pop_pdf controls/pdf/one-page.pdf
```

# pdf.js-extract — PDF / JavaScript

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `new PDFExtract().extractBuffer(Buffer, {})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf.js-extract>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Direct or transitive PDF.js use, fork, or redistribution; package count does not imply an independent parser engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf_js_extract/README.md)

```sh
python3 parsarium.py build pdf javascript pdf_js_extract
python3 parsarium.py run pdf javascript pdf_js_extract controls/pdf/one-page.pdf
```

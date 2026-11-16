# pdf-ts — PDF / JavaScript

- **Pinned release:** `0.0.2`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `pdfToText(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf-ts>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf_ts/README.md)

```sh
python3 parsarium.py build pdf javascript pdf_ts
python3 parsarium.py run pdf javascript pdf_ts controls/pdf/one-page.pdf
```

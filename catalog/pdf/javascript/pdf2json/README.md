# pdf2json — PDF / JavaScript

- **Pinned release:** `4.1.1`
- **License:** Apache-2.0
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `new PDFParser().parseBuffer(Buffer); pdfParser_dataReady event`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf2json>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf2json/README.md)

```sh
python3 parsarium.py build pdf javascript pdf2json
python3 parsarium.py run pdf javascript pdf2json controls/pdf/one-page.pdf
```

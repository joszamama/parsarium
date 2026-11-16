# pdf-text-reader — PDF / JavaScript

- **Pinned release:** `5.1.1`
- **License:** (MIT or CC0 1.0)
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `readPdfText({url:localPath})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf-text-reader>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf_text_reader/README.md)

```sh
python3 parsarium.py build pdf javascript pdf_text_reader
python3 parsarium.py run pdf javascript pdf_text_reader controls/pdf/one-page.pdf
```

# pdf-parser.js — PDF / JavaScript

- **Pinned release:** `5.8.5`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** pdf-parser.js
- **Local input API:** `readPdf(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdf-parser.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf_parser_js/README.md)

```sh
python3 parsarium.py build pdf javascript pdf_parser_js
python3 parsarium.py run pdf javascript pdf_parser_js controls/pdf/one-page.pdf
```

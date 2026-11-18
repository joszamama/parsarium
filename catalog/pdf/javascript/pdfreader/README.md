# pdfreader — PDF / JavaScript

- **Pinned release:** `3.0.8`
- **Upstream:** [source repository](<https://github.com/adrienjoly/npm-pdfreader>) · [npm](<https://www.npmjs.com/package/pdfreader>)
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `new PdfReader().parseBuffer(Buffer, callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdfreader>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Depends on pdf2json, a PDF.js-derived parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdfreader/README.md)

```sh
python3 parsarium.py build pdf javascript pdfreader
python3 parsarium.py run pdf javascript pdfreader controls/pdf/one-page.pdf
```

# afpp — PDF / JavaScript

- **Pinned release:** `3.3.0`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `pdf2string(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/afpp>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/afpp/README.md)

```sh
python3 parsarium.py build pdf javascript afpp
python3 parsarium.py run pdf javascript afpp controls/pdf/one-page.pdf
```

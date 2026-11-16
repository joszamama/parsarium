# officeparser — PDF / JavaScript

- **Pinned release:** `8.4.0`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `OfficeParser.parseOffice(Buffer); ast.to("text")`
- **Documentation:** [API reference](<https://www.npmjs.com/package/officeparser>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/officeparser/README.md)

```sh
python3 parsarium.py build pdf javascript officeparser
python3 parsarium.py run pdf javascript officeparser controls/pdf/one-page.pdf
```

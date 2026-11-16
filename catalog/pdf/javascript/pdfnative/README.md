# pdfnative — PDF / JavaScript

- **Pinned release:** `1.9.0`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** pdfnative
- **Local input API:** `extractText(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdfnative>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdfnative/README.md)

```sh
python3 parsarium.py build pdf javascript pdfnative
python3 parsarium.py run pdf javascript pdfnative controls/pdf/one-page.pdf
```

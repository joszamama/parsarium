# pdfnano — PDF / JavaScript

- **Pinned release:** `0.2.11`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** pdfnano
- **Local input API:** `new PDFParser().parseFile(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pdfnano>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdfnano/README.md)

```sh
python3 parsarium.py build pdf javascript pdfnano
python3 parsarium.py run pdf javascript pdfnano controls/pdf/one-page.pdf
```

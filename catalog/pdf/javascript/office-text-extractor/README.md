# office-text-extractor — PDF / JavaScript

- **Pinned release:** `4.0.0`
- **License:** ISC
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `getTextExtractor().extractText({input:Buffer,type:"buffer"})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/office-text-extractor>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Depends on pdf-parse@2.4.5, which uses PDF.js.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/office_text_extractor/README.md)

```sh
python3 parsarium.py build pdf javascript office_text_extractor
python3 parsarium.py run pdf javascript office_text_extractor controls/pdf/one-page.pdf
```

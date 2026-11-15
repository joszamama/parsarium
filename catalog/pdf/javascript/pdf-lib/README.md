# pdf-lib — PDF / JavaScript

- **Pinned release:** `1.17.1`
- **License:** MIT
- **Parsed scope:** page_metadata
- **Underlying family:** pdf-lib
- **Local input API:** `PDFDocument.load(Buffer); getPageCount(); getTitle()`
- **Documentation:** [API reference](<https://pdf-lib.js.org/docs/api/classes/pdfdocument>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/pdf_lib/README.md)

```sh
python3 parsarium.py build pdf javascript pdf_lib
python3 parsarium.py run pdf javascript pdf_lib controls/pdf/one-page.pdf
```

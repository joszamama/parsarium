# pdfjs-dist — PDF / JavaScript

- **Pinned release:** `6.5.438`
- **License:** Apache-2.0
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `getDocument({data:Uint8Array}).promise; getPage(1).getTextContent()`
- **Documentation:** [API reference](<https://mozilla.github.io/pdf.js/api/draft/module-pdfjsLib.html>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

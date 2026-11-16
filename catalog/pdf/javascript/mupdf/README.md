# mupdf — PDF / JavaScript

- **Pinned release:** `1.28.6`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** text
- **Underlying family:** MuPDF
- **Local input API:** `Document.openDocument(path); loadPage(0).toStructuredText().asText()`
- **Documentation:** [API reference](<https://mupdf.readthedocs.io/en/latest/reference/javascript/>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

WASM binding around MuPDF.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

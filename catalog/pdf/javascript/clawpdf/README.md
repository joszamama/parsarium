# clawpdf — PDF / JavaScript

- **Pinned release:** `0.3.2`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** PDFium
- **Local input API:** `openPdf(path).page(1).text()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/clawpdf>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

WASM binding around PDFium.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# @firecrawl/pdf-inspector-wasm — PDF / JavaScript

- **Pinned release:** `1.25.2`
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** pdf-inspector
- **Local input API:** `extractText(Uint8Array) after local WASM init`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@firecrawl/pdf-inspector-wasm>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/firecrawl_pdf_inspector_wasm/README.md)

```sh
python3 parsarium.py build pdf javascript firecrawl_pdf_inspector_wasm
python3 parsarium.py run pdf javascript firecrawl_pdf_inspector_wasm controls/pdf/one-page.pdf
```

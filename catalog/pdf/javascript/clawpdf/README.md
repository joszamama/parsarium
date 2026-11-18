# clawpdf — PDF / JavaScript

- **Pinned release:** `0.3.2`
- **Upstream:** [source repository](<https://github.com/openclaw/clawpdf>) · [npm](<https://www.npmjs.com/package/clawpdf>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/clawpdf/README.md)

```sh
python3 parsarium.py build pdf javascript clawpdf
python3 parsarium.py run pdf javascript clawpdf controls/pdf/one-page.pdf
```

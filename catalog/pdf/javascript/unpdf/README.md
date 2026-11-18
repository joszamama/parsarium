# unpdf — PDF / JavaScript

- **Pinned release:** `2.1.0`
- **Upstream:** [source repository](<https://github.com/unjs/unpdf>) · [npm](<https://www.npmjs.com/package/unpdf>)
- **License:** MIT
- **Parsed scope:** text
- **Underlying family:** mozilla/pdf.js
- **Local input API:** `extractText(Uint8Array, {mergePages:true})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/unpdf>)
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

[Docker harness and verification receipt](../../../../projects/pdf/javascript/unpdf/README.md)

```sh
python3 parsarium.py build pdf javascript unpdf
python3 parsarium.py run pdf javascript unpdf controls/pdf/one-page.pdf
```

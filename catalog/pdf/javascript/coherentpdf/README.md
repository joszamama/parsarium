# coherentpdf — PDF / JavaScript

- **Pinned release:** `2.5.5`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** page_count
- **Underlying family:** coherentpdf
- **Local input API:** `fromFile(path, ""); pages(pdf)`
- **Documentation:** [API reference](<https://www.coherentpdf.com/jscpdf/index.html>)
- **Catalog evidence:** [parser record](../../../../data/javascript/pdf/parsers.json) · [control verification](../../../../data/javascript/pdf/verification.json) · [within-ecosystem ranking](../../../../data/javascript/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/javascript/coherentpdf/README.md)

```sh
python3 parsarium.py build pdf javascript coherentpdf
python3 parsarium.py run pdf javascript coherentpdf controls/pdf/one-page.pdf
```

# PyMuPDF — PDF / Python

- **Pinned release:** `2.1`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** page text
- **Underlying family:** MuPDF
- **Local input API:** `pymupdf.open(local path)`
- **Documentation:** [API reference](<https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pymupdf/README.md)

```sh
python3 parsarium.py build pdf python pymupdf
python3 parsarium.py run pdf python pymupdf controls/pdf/one-page.pdf
```

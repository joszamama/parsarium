# PyPDF4 — PDF / Python

- **Pinned release:** `1.27.0`
- **License:** BSD
- **Parsed scope:** page count and document title
- **Underlying family:** PyPDF4 fork of PyPDF2/pypdf family
- **Local input API:** `PyPDF4.PdfFileReader(local byte stream)`
- **Documentation:** [API reference](<https://pypi.org/project/PyPDF4/1.27.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pypdf4/README.md)

```sh
python3 parsarium.py build pdf python pypdf4
python3 parsarium.py run pdf python pypdf4 controls/pdf/one-page.pdf
```

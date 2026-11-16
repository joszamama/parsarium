# pypdfium2 — PDF / Python

- **Pinned release:** `5.10.1`
- **License:** BSD-3-Clause
- **Parsed scope:** page text
- **Underlying family:** PDFium
- **Local input API:** `pypdfium2.PdfDocument(local path)`
- **Documentation:** [API reference](<https://pypdfium2.readthedocs.io/en/stable/python_api.html>)
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

[Docker harness and verification receipt](../../../../projects/pdf/python/pypdfium2/README.md)

```sh
python3 parsarium.py build pdf python pypdfium2
python3 parsarium.py run pdf python pypdfium2 controls/pdf/one-page.pdf
```

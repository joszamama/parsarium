# pypdf — PDF / Python

- **Pinned release:** `7.0.1`
- **License:** BSD-3-Clause
- **Parsed scope:** page text
- **Underlying family:** pypdf pure Python
- **Local input API:** `pypdf.PdfReader(local path)`
- **Documentation:** [API reference](<https://pypdf.readthedocs.io/en/latest/modules/PdfReader.html>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "text": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

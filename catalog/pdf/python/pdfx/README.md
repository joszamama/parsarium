# pdfx — PDF / Python

- **Pinned release:** `1.4.1`
- **License:** Apache-2.0
- **Parsed scope:** page count and document title
- **Underlying family:** PDFx via pdfminer.six 20201018
- **Local input API:** `pdfx.PDFx(local path).get_metadata()`
- **Documentation:** [API reference](<https://pypi.org/project/pdfx/1.4.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

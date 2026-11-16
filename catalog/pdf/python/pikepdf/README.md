# pikepdf — PDF / Python

- **Pinned release:** `10.18.0`
- **License:** MPL-2.0
- **Parsed scope:** page count and document title
- **Underlying family:** QPDF
- **Local input API:** `pikepdf.open(local path)`
- **Documentation:** [API reference](<https://pikepdf.readthedocs.io/en/latest/tutorial.html>)
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

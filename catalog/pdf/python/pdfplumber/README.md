# pdfplumber — PDF / Python

- **Pinned release:** `0.11.10`
- **License:** MIT
- **Parsed scope:** page text
- **Underlying family:** pdfplumber via pdfminer.six
- **Local input API:** `pdfplumber.open(local path)`
- **Documentation:** [API reference](<https://github.com/jsvine/pdfplumber>)
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

# pdfrw — PDF / Python

- **Pinned release:** `0.4`
- **License:** MIT
- **Parsed scope:** page count and document title
- **Underlying family:** pdfrw parser
- **Local input API:** `pdfrw.PdfReader(local path)`
- **Documentation:** [API reference](<https://github.com/pmaupin/pdfrw>)
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

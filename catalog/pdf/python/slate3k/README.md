# slate3k — PDF / Python

- **Pinned release:** `0.5.3`
- **License:** MIT
- **Parsed scope:** page text
- **Underlying family:** Slate3k via pdfminer3k
- **Local input API:** `slate3k.PDF(local byte stream)`
- **Documentation:** [API reference](<https://pypi.org/project/slate3k/0.5.3/>)
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

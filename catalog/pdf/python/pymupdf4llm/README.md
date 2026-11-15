# pymupdf4llm — PDF / Python

- **Pinned release:** `2.1`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** page text as Markdown
- **Underlying family:** PyMuPDF4LLM via MuPDF
- **Local input API:** `pymupdf4llm.to_markdown(local path)`
- **Documentation:** [API reference](<https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/api.html>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

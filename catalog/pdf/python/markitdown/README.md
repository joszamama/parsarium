# markitdown — PDF / Python

- **Pinned release:** `0.1.9`
- **License:** MIT
- **Parsed scope:** page text as Markdown
- **Underlying family:** MarkItDown via pdfplumber/pdfminer.six
- **Local input API:** `markitdown.MarkItDown().convert(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/markitdown/0.1.9/>)
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

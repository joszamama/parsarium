# github.com/go-pdfkit/extract — PDF / Go

- **Pinned release:** `v0.11.0`
- **License:** BSD-3-Clause
- **Parsed scope:** page text
- **Underlying family:** go-pdfkit reader family
- **Local input API:** `reader.Open([]byte); extract.Text(*reader.Document, 1)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-pdfkit/extract@v0.11.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Shared code lineage; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

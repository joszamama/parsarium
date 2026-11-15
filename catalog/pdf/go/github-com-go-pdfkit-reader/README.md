# github.com/go-pdfkit/reader — PDF / Go

- **Pinned release:** `v0.10.0`
- **License:** BSD-3-Clause
- **Parsed scope:** page count
- **Underlying family:** go-pdfkit reader family
- **Local input API:** `Open([]byte).PageCount()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-pdfkit/reader@v0.10.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Shared code lineage; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

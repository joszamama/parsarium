# github.com/dcu/pdf — PDF / Go

- **Pinned release:** `v0.0.0-20190612170416-c8b299d05f89`
- **License:** BSD-3-Clause
- **Parsed scope:** page count
- **Underlying family:** rsc PDF reader lineage
- **Local input API:** `NewReader(io.ReaderAt, size).NumPage()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dcu/pdf@v0.0.0-20190612170416-c8b299d05f89>)
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

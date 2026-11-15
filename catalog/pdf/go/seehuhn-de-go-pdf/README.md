# seehuhn.de/go/pdf — PDF / Go

- **Pinned release:** `v0.8.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF version
- **Underlying family:** seehuhn PDF reader
- **Local input API:** `NewReader(io.ReaderAt, size, nil).GetMeta().Version`
- **Documentation:** [API reference](<https://pkg.go.dev/seehuhn.de/go/pdf@v0.8.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "version": "1.4"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

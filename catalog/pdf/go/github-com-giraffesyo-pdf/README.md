# github.com/giraffesyo/pdf — PDF / Go

- **Pinned release:** `v0.9.0`
- **License:** Apache-2.0
- **Parsed scope:** page count
- **Underlying family:** giraffesyo PDF extractor
- **Local input API:** `Extract(context.Context, io.ReaderAt, size).PageCount`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/giraffesyo/pdf@v0.9.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

# github.com/gen2brain/go-fitz — PDF / Go

- **Pinned release:** `v1.28.2`
- **License:** AGPL-3.0
- **Parsed scope:** page count
- **Underlying family:** MuPDF via go-fitz
- **Local input API:** `NewFromMemory([]byte).NumPage()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gen2brain/go-fitz@v1.28.2>)
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

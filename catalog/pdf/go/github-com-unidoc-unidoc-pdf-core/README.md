# github.com/unidoc/unidoc/pdf/core — PDF / Go

- **Pinned release:** `v2.2.0+incompatible`
- **License:** AGPL-3.0 or commercial (AGPL option used for open-source qualification)
- **Parsed scope:** PDF indirect object count
- **Underlying family:** UniDoc core
- **Local input API:** `NewParser(io.ReadSeeker).GetObjectNums()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unidoc/unidoc/pdf/core@v2.2.0+incompatible>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "objects": 6
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

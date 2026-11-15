# github.com/tetsuo/mp4 — MP4 / Go

- **Pinned release:** `v0.3.0`
- **License:** MIT
- **Parsed scope:** ftyp brand only
- **Underlying family:** tetsuo MP4 box reader
- **Local input API:** `NewReader([]byte).Next(); ReadFtyp([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tetsuo/mp4@v0.3.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

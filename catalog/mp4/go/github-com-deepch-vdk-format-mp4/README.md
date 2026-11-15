# github.com/deepch/vdk/format/mp4 — MP4 / Go

- **Pinned release:** `v0.0.27`
- **License:** MIT
- **Parsed scope:** stream count
- **Underlying family:** joy4 MP4 lineage
- **Local input API:** `NewDemuxer(io.ReadSeeker).Streams()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/deepch/vdk/format/mp4@v0.0.27>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "streams": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

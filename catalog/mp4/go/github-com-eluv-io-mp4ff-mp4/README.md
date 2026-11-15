# github.com/eluv-io/mp4ff/mp4 — MP4 / Go

- **Pinned release:** `v0.48.0`
- **License:** MIT, MIT
- **Parsed scope:** brand and track count
- **Underlying family:** mp4ff lineage
- **Local input API:** `DecodeFile(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/eluv-io/mp4ff/mp4@v0.48.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "tracks": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

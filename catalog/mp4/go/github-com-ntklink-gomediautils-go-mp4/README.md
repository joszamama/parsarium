# github.com/ntklink/gomediautils/go-mp4 — MP4 / Go

- **Pinned release:** `v0.0.0-20260924103313-787406a6c4b3`
- **License:** MIT
- **Parsed scope:** track count
- **Underlying family:** gomedia MP4 lineage
- **Local input API:** `CreateMp4Demuxer(io.ReadSeeker).ReadHead()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ntklink/gomediautils/go-mp4@v0.0.0-20260924103313-787406a6c4b3>)
- **Catalog evidence:** [parser record](../../../../data/go/mp4/parsers.json) · [control verification](../../../../data/go/mp4/verification.json) · [within-ecosystem ranking](../../../../data/go/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

Shared code lineage; package count does not imply independent parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

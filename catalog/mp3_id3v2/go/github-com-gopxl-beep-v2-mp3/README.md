# github.com/gopxl/beep/v2/mp3 — MP3 with ID3v2 / Go

- **Pinned release:** `v2.1.1`
- **License:** MIT
- **Parsed scope:** decoded samples and sample rate
- **Underlying family:** hajime/go-mp3 via beep
- **Local input API:** `Decode(io.ReadCloser); Stream(samples)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gopxl/beep/v2/mp3@v2.1.1>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3_id3v2/parsers.json) · [control verification](../../../../data/go/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "samples": 16
}
```

Shared parser lineage; package paths do not imply independent decoder engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

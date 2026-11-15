# github.com/qiniu/audio/wav — WAV / Go

- **Pinned release:** `v0.2.1`
- **License:** Apache-2.0
- **Parsed scope:** decoded_bytes
- **Underlying family:** qiniu WAV reader
- **Local input API:** `Decode(io.ReadSeeker)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/qiniu/audio/wav@v0.2.1>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_bytes": 8
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

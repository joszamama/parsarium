# github.com/ngyewch/go-pcm/wav — WAV / Go

- **Pinned release:** `v0.3.0`
- **License:** MIT
- **Parsed scope:** data_bytes
- **Underlying family:** go-pcm WAV reader
- **Local input API:** `NewReader(path); Read([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ngyewch/go-pcm/wav@v0.3.0>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "data_bytes": 8
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

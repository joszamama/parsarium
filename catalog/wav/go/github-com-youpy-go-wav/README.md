# github.com/youpy/go-wav — WAV / Go

- **Pinned release:** `v0.3.2`
- **License:** ISC
- **Parsed scope:** signs
- **Underlying family:** youpy WAV reader
- **Local input API:** `NewReader(io.ReaderAt); Format(); ReadSamples()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/youpy/go-wav@v0.3.2>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16,
  "signs": [
    0,
    1,
    -1,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

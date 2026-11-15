# github.com/moutend/go-wav — WAV / Go

- **Pinned release:** `v0.0.0-20170820031854-56127fbbb7ba`
- **License:** MIT
- **Parsed scope:** signs
- **Underlying family:** moutend WAV reader
- **Local input API:** `Unmarshal([]byte,*File)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/moutend/go-wav@v0.0.0-20170820031854-56127fbbb7ba>)
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

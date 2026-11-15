# github.com/200sc/klangsynthese/wav — WAV / Go

- **Pinned release:** `v0.2.1`
- **License:** Apache-2.0
- **Parsed scope:** data_bytes
- **Underlying family:** klangsynthese WAV reader
- **Local input API:** `Read(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/200sc/klangsynthese/wav@v0.2.1>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16,
  "data_bytes": 8
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

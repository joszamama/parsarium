# github.com/cryptix/wav — WAV / Go

- **Pinned release:** `v0.0.0-20180415113528-8bdace674401`
- **License:** GPL-2.0
- **Parsed scope:** sample_count
- **Underlying family:** cryptix WAV reader
- **Local input API:** `NewReader(io.ReadSeeker,size); GetSampleCount()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cryptix/wav@v0.0.0-20180415113528-8bdace674401>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16,
  "sample_count": 4
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

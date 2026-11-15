# github.com/xigh/go-wavreader — WAV / Go

- **Pinned release:** `v0.0.0-20210516212152-f49019aa7352`
- **License:** MIT
- **Parsed scope:** frames
- **Underlying family:** xigh WAV reader
- **Local input API:** `New(io.ReaderAt); Rate(); Chans(); Len()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/xigh/go-wavreader@v0.0.0-20210516212152-f49019aa7352>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

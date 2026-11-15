# github.com/hajimehoshi/ebiten/v2/audio/wav — WAV / Go

- **Pinned release:** `v2.10.6`
- **License:** Apache-2.0
- **Parsed scope:** decoded_stereo_bytes
- **Underlying family:** Ebitengine WAV decoder
- **Local input API:** `DecodeWithoutResampling(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/wav@v2.10.6>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "decoded_stereo_bytes": 16
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

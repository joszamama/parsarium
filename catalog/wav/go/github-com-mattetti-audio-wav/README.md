# github.com/mattetti/audio/wav — WAV / Go

- **Pinned release:** `v0.0.0-20240411020228-c5379f9b5b61`
- **Upstream:** [source repository](<https://github.com/mattetti/audio>) · [pkg.go.dev](<https://pkg.go.dev/github.com/mattetti/audio/wav>)
- **License:** MIT
- **Parsed scope:** signs
- **Underlying family:** mattetti/go-audio WAV lineage
- **Local input API:** `NewDecoder(io.ReadSeeker); FullPCMBuffer()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/mattetti/audio/wav@v0.0.0-20240411020228-c5379f9b5b61>)
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

Shared underlying parser lineage; package count is not an independent engine count.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_mattetti_audio_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_mattetti_audio_wav
python3 parsarium.py run wav go github_com_mattetti_audio_wav controls/wav/four-samples.wav
```

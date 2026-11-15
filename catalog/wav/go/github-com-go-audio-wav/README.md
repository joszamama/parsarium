# github.com/go-audio/wav — WAV / Go

- **Pinned release:** `v1.1.0`
- **License:** Apache-2.0
- **Parsed scope:** signs
- **Underlying family:** mattetti/go-audio WAV lineage
- **Local input API:** `NewDecoder(io.ReadSeeker); FullPCMBuffer()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-audio/wav@v1.1.0>)
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

[Docker harness and verification receipt](../../../../projects/wav/go/go_audio_wav/README.md)

```sh
python3 parsarium.py build wav go go_audio_wav
python3 parsarium.py run wav go go_audio_wav controls/wav/four-samples.wav
```

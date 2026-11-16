# github.com/faiface/beep/wav — WAV / Go

- **Pinned release:** `v1.1.0`
- **License:** MIT
- **Parsed scope:** signs
- **Underlying family:** beep WAV lineage
- **Local input API:** `Decode(io.Reader); Stream()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/faiface/beep/wav@v1.1.0>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
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

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_faiface_beep_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_faiface_beep_wav
python3 parsarium.py run wav go github_com_faiface_beep_wav controls/wav/four-samples.wav
```

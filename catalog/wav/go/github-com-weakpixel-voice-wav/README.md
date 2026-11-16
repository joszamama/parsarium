# github.com/weakpixel/voice/wav — WAV / Go

- **Pinned release:** `v0.0.1`
- **License:** MIT
- **Parsed scope:** signs
- **Underlying family:** weakpixel WAV reader
- **Local input API:** `Read(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/weakpixel/voice/wav@v0.0.1>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "signs": [
    0,
    1,
    -1,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_weakpixel_voice_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_weakpixel_voice_wav
python3 parsarium.py run wav go github_com_weakpixel_voice_wav controls/wav/four-samples.wav
```

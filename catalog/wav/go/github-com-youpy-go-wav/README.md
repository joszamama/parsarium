# github.com/youpy/go-wav — WAV / Go

- **Pinned release:** `v0.3.2`
- **Upstream:** [source repository](<https://github.com/youpy/go-wav>) · [pkg.go.dev](<https://pkg.go.dev/github.com/youpy/go-wav>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_youpy_go_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_youpy_go_wav
python3 parsarium.py run wav go github_com_youpy_go_wav controls/wav/four-samples.wav
```

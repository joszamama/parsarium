# github.com/yut-kt/gowave — WAV / Go

- **Pinned release:** `v0.1.4`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** gowave reader
- **Local input API:** `New(io.ReadSeeker); GetSampleRate(); GetNumChannels()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/yut-kt/gowave@v0.1.4>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_yut_kt_gowave/README.md)

```sh
python3 parsarium.py build wav go github_com_yut_kt_gowave
python3 parsarium.py run wav go github_com_yut_kt_gowave controls/wav/four-samples.wav
```

# github.com/iFaceless/godub/wav — WAV / Go

- **Pinned release:** `v0.0.0-20200728093528-a30bb4d1a0f1`
- **License:** MIT
- **Parsed scope:** data_bytes
- **Underlying family:** godub WAV reader
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/iFaceless/godub/wav@v0.0.0-20200728093528-a30bb4d1a0f1>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_ifaceless_godub_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_ifaceless_godub_wav
python3 parsarium.py run wav go github_com_ifaceless_godub_wav controls/wav/four-samples.wav
```

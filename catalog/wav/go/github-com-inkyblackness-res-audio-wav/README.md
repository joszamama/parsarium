# github.com/inkyblackness/res/audio/wav — WAV / Go

- **Pinned release:** `v0.0.0-20180728072643-e78e2ff1969d`
- **License:** BSD-3-Clause
- **Parsed scope:** sample_count
- **Underlying family:** inkyblackness WAV decoder
- **Local input API:** `Load(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/inkyblackness/res/audio/wav@v0.0.0-20180728072643-e78e2ff1969d>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "sample_count": 4
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_inkyblackness_res_audio_wav/README.md)

```sh
python3 parsarium.py build wav go github_com_inkyblackness_res_audio_wav
python3 parsarium.py run wav go github_com_inkyblackness_res_audio_wav controls/wav/four-samples.wav
```

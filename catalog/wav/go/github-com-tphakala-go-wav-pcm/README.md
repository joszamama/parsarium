# github.com/tphakala/go-wav/pcm — WAV / Go

- **Pinned release:** `v1.1.1`
- **License:** MIT
- **Parsed scope:** data_bytes
- **Underlying family:** tphakala WAV reader
- **Local input API:** `DecodeInterleavedBytes([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tphakala/go-wav/pcm@v1.1.1>)
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

[Docker harness and verification receipt](../../../../projects/wav/go/github_com_tphakala_go_wav_pcm/README.md)

```sh
python3 parsarium.py build wav go github_com_tphakala_go_wav_pcm
python3 parsarium.py run wav go github_com_tphakala_go_wav_pcm controls/wav/four-samples.wav
```

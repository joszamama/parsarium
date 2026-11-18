# azul3d.org/engine/audio/wav — WAV / Go

- **Pinned release:** `v0.0.0-20211024043305-793ea6c2839d`
- **Upstream:** [pkg.go.dev](<https://pkg.go.dev/azul3d.org/engine/audio/wav>)
- **License:** BSD-3-Clause
- **Parsed scope:** format
- **Underlying family:** azul3d WAV decoder
- **Local input API:** `audio.NewDecoder(io.Reader) with wav registered`
- **Documentation:** [API reference](<https://pkg.go.dev/azul3d.org/engine/audio/wav@v0.0.0-20211024043305-793ea6c2839d>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/go/azul3d_org_engine_audio_wav/README.md)

```sh
python3 parsarium.py build wav go azul3d_org_engine_audio_wav
python3 parsarium.py run wav go azul3d_org_engine_audio_wav controls/wav/four-samples.wav
```

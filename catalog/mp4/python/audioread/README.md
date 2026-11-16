# audioread — MP4 / Python

- **Pinned release:** `3.1.0`
- **License:** MIT
- **Parsed scope:** AAC audio properties
- **Underlying family:** audioread via FFmpeg
- **Local input API:** `audioread.audio_open(local path)`
- **Documentation:** [API reference](<https://github.com/beetbox/audioread>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "audio_rate": 8000,
  "audio_channels": 1,
  "duration_seconds": 1.0
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/audioread/README.md)

```sh
python3 parsarium.py build mp4 python audioread
python3 parsarium.py run mp4 python audioread controls/mp4/red-av.mp4
```

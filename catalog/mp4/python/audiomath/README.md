# audiomath — MP4 / Python

- **Pinned release:** `1.23.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** AAC audio decode
- **Underlying family:** audiomath via audioread/FFmpeg
- **Local input API:** `audiomath.Sound(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/audiomath/1.23.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp4/parsers.json) · [control verification](../../../../data/python/mp4/verification.json) · [within-ecosystem ranking](../../../../data/python/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "audio_rate": 8000,
  "audio_samples": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/python/audiomath/README.md)

```sh
python3 parsarium.py build mp4 python audiomath
python3 parsarium.py run mp4 python audiomath controls/mp4/red-av.mp4
```

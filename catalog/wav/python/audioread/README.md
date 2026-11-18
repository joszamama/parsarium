# audioread — WAV / Python

- **Pinned release:** `3.1.0`
- **Upstream:** [source repository](<https://github.com/beetbox/audioread>) · [PyPI](<https://pypi.org/project/audioread/>)
- **License:** MIT
- **Parsed scope:** PCM samples
- **Underlying family:** audioread rawread via CPython wave
- **Local input API:** `audioread.audio_open(local path); iterate PCM chunks`
- **Documentation:** [API reference](<https://github.com/beetbox/audioread>)
- **Catalog evidence:** [parser record](../../../../data/python/wav/parsers.json) · [control verification](../../../../data/python/wav/verification.json) · [within-ecosystem ranking](../../../../data/python/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/audioread/README.md)

```sh
python3 parsarium.py build wav python audioread
python3 parsarium.py run wav python audioread controls/wav/four-samples.wav
```

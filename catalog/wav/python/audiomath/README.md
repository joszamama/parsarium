# audiomath — WAV / Python

- **Pinned release:** `1.23.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** PCM samples
- **Underlying family:** audiomath WAV loader via CPython wave
- **Local input API:** `audiomath.Sound(local path).y`
- **Documentation:** [API reference](<https://pypi.org/project/audiomath/1.23.0/>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

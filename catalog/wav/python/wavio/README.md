# wavio — WAV / Python

- **Pinned release:** `0.0.9`
- **License:** BSD-2-Clause
- **Parsed scope:** PCM samples
- **Underlying family:** wavio via CPython wave
- **Local input API:** `wavio.read(local path)`
- **Documentation:** [API reference](<https://github.com/WarrenWeckesser/wavio>)
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

[Docker harness and verification receipt](../../../../projects/wav/python/wavio/README.md)

```sh
python3 parsarium.py build wav python wavio
python3 parsarium.py run wav python wavio controls/wav/four-samples.wav
```

# audiolab — WAV / Python

- **Pinned release:** `0.5.2`
- **License:** Apache-2.0
- **Parsed scope:** PCM samples
- **Underlying family:** audiolab via soundfile/libsndfile
- **Local input API:** `audiolab.load_audio(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/audiolab/0.5.2/>)
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

# audiofile — WAV / Python

- **Pinned release:** `1.6.1`
- **License:** MIT
- **Parsed scope:** PCM samples
- **Underlying family:** audiofile via soundfile/libsndfile
- **Local input API:** `audiofile.read(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/audiofile/1.6.1/>)
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

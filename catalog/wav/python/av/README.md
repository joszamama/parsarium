# av — WAV / Python

- **Pinned release:** `19.0.2`
- **License:** BSD-3-Clause
- **Parsed scope:** PCM samples
- **Underlying family:** FFmpeg libavformat/libavcodec via PyAV
- **Local input API:** `av.open(local path).decode(audio=0)`
- **Documentation:** [API reference](<https://pyav.org/docs/stable/api/container.html>)
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

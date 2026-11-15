# pygame — WAV / Python

- **Pinned release:** `2.6.1`
- **License:** LGPL
- **Parsed scope:** PCM samples
- **Underlying family:** pygame SDL_mixer WAV loader
- **Local input API:** `pygame.mixer.Sound(local path).get_raw()`
- **Documentation:** [API reference](<https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound>)
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

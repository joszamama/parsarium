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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/python/pygame/README.md)

```sh
python3 parsarium.py build wav python pygame
python3 parsarium.py run wav python pygame controls/wav/four-samples.wav
```

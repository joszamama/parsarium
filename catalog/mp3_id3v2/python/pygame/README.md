# pygame — MP3 with ID3v2 / Python

- **Pinned release:** `2.6.1`
- **License:** LGPL
- **Parsed scope:** decoded audio duration
- **Underlying family:** SDL_mixer MP3 decoder
- **Local input API:** `pygame.mixer.Sound(local path)`
- **Documentation:** [API reference](<https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_ms": 1000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/pygame/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python pygame
python3 parsarium.py run mp3_id3v2 python pygame controls/mp3_id3v2/tone-tags.mp3
```

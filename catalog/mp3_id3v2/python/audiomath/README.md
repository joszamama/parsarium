# audiomath — MP3 with ID3v2 / Python

- **Pinned release:** `1.23.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** decoded PCM sample count
- **Underlying family:** audiomath via audioread/FFmpeg
- **Local input API:** `audiomath.Sound(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/audiomath/1.23.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "samples": 9216
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/audiomath/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python audiomath
python3 parsarium.py run mp3_id3v2 python audiomath controls/mp3_id3v2/tone-tags.mp3
```

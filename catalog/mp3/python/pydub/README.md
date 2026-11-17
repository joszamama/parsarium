# pydub — MP3 / Python

- **Pinned release:** `0.25.1`
- **License:** MIT
- **Parsed scope:** decoded duration and audio properties
- **Underlying family:** pydub via FFmpeg
- **Local input API:** `pydub.AudioSegment.from_mp3(local path)`
- **Documentation:** [API reference](<https://github.com/jiaaro/pydub>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control verification](../../../../data/python/mp3/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "duration_ms": 1000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/python/pydub/README.md)

```sh
python3 parsarium.py build mp3 python pydub
python3 parsarium.py run mp3 python pydub controls/mp3/id3v2-tagged-tone.mp3
```

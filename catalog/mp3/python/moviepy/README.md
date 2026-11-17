# moviepy — MP3 / Python

- **Pinned release:** `2.2.1`
- **License:** MIT
- **Parsed scope:** decoded audio and duration
- **Underlying family:** MoviePy via bundled FFmpeg
- **Local input API:** `moviepy.AudioFileClip(local path)`
- **Documentation:** [API reference](<https://github.com/Zulko/moviepy/blob/master/moviepy/audio/io/AudioFileClip.py>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control verification](../../../../data/python/mp3/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_seconds": 1.0,
  "decoded_audio": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/moviepy/README.md)

```sh
python3 parsarium.py build mp3 python moviepy
python3 parsarium.py run mp3 python moviepy controls/mp3_id3v2/tone-tags.mp3
```

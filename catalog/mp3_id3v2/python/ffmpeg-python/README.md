# ffmpeg-python — MP3 with ID3v2 / Python

- **Pinned release:** `0.2.0`
- **License:** Apache-2.0
- **Parsed scope:** ID3v2 tags and MPEG codec
- **Underlying family:** ffmpeg-python via external FFprobe
- **Local input API:** `ffmpeg.probe(local path)`
- **Documentation:** [API reference](<https://github.com/kkroening/ffmpeg-python>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "codec": "mp3"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/ffmpeg_python/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python ffmpeg_python
python3 parsarium.py run mp3_id3v2 python ffmpeg_python controls/mp3_id3v2/tone-tags.mp3
```

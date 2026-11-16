# av — MP3 with ID3v2 / Python

- **Pinned release:** `19.0.2`
- **License:** BSD-3-Clause
- **Parsed scope:** ID3v2 tags and MP3 audio stream
- **Underlying family:** FFmpeg libavformat via PyAV
- **Local input API:** `av.open(local path)`
- **Documentation:** [API reference](<https://pyav.org/docs/stable/api/container.html>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sample_rate": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/av/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python av
python3 parsarium.py run mp3_id3v2 python av controls/mp3_id3v2/tone-tags.mp3
```

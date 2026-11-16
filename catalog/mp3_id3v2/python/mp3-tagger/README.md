# mp3-tagger — MP3 with ID3v2 / Python

- **Pinned release:** `1.0`
- **License:** MIT
- **Parsed scope:** ID3v2 title, artist, album
- **Underlying family:** mp3-tagger ID3 parser
- **Local input API:** `mp3_tagger.MP3File(local path); set_version(VERSION_2)`
- **Documentation:** [API reference](<https://pypi.org/project/mp3-tagger/1.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/mp3_id3v2/parsers.json) · [control verification](../../../../data/python/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/python/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/mp3_tagger/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python mp3_tagger
python3 parsarium.py run mp3_id3v2 python mp3_tagger controls/mp3_id3v2/tone-tags.mp3
```

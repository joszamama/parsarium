# chemz — MP3 with ID3v2 / Python

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** ID3v2 tags and MP3 sample rate
- **Underlying family:** chemz via Mutagen
- **Local input API:** `chemz.read_track(local Path)`
- **Documentation:** [API reference](<https://pypi.org/project/chemz/0.1.0/>)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/python/chemz/README.md)

```sh
python3 parsarium.py build mp3_id3v2 python chemz
python3 parsarium.py run mp3_id3v2 python chemz controls/mp3_id3v2/tone-tags.mp3
```

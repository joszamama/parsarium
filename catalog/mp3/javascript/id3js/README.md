# id3js — MP3 / JavaScript

- **Pinned release:** `2.1.1`
- **License:** MIT
- **Parsed scope:** tags+version
- **Underlying family:** id3js
- **Local input API:** `fromPath(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/id3js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "version": [
    3,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/id3js/README.md)

```sh
python3 parsarium.py build mp3 javascript id3js
python3 parsarium.py run mp3 javascript id3js controls/mp3_id3v2/tone-tags.mp3
```

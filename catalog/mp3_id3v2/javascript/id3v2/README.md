# id3v2 — MP3 with ID3v2 / JavaScript

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** id3v2
- **Local input API:** `new ID3v2(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/id3v2>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/id3v2/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript id3v2
python3 parsarium.py run mp3_id3v2 javascript id3v2 controls/mp3_id3v2/tone-tags.mp3
```

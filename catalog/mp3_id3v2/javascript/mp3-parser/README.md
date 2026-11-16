# mp3-parser — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** tags+version
- **Underlying family:** mp3-parser
- **Local input API:** `readId3v2Tag(DataView)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp3-parser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "version": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/mp3_parser/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript mp3_parser
python3 parsarium.py run mp3_id3v2 javascript mp3_parser controls/mp3_id3v2/tone-tags.mp3
```

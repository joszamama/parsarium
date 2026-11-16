# mp3tag — MP3 with ID3v2 / JavaScript

- **Pinned release:** `1.0.5`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** mp3tag
- **Local input API:** `readHeader(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp3tag>)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/mp3tag/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript mp3tag
python3 parsarium.py run mp3_id3v2 javascript mp3tag controls/mp3_id3v2/tone-tags.mp3
```

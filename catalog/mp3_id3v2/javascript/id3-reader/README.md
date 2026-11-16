# id3-reader — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.0.2`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** id3-reader
- **Local input API:** `reader(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/id3-reader>)
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

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/id3_reader/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript id3_reader
python3 parsarium.py run mp3_id3v2 javascript id3_reader controls/mp3_id3v2/tone-tags.mp3
```

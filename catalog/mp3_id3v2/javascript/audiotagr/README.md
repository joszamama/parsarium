# audiotagr — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.2.0`
- **License:** LGPL-3.0-only
- **Parsed scope:** tags
- **Underlying family:** music-metadata
- **Local input API:** `readAudioMetadata(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/audiotagr>)
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

Read path delegates to its pinned music-metadata dependency.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/audiotagr/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript audiotagr
python3 parsarium.py run mp3_id3v2 javascript audiotagr controls/mp3_id3v2/tone-tags.mp3
```

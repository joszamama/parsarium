# get-mp3-duration — MP3 with ID3v2 / JavaScript

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** get-mp3-duration
- **Local input API:** `getMP3Duration(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/get-mp3-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_ms": 1224
}
```

Frame duration includes MP3 padding and differs from nominal one-second source duration.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/get_mp3_duration/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript get_mp3_duration
python3 parsarium.py run mp3_id3v2 javascript get_mp3_duration controls/mp3_id3v2/tone-tags.mp3
```

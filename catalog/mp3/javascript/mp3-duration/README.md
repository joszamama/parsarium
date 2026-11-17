# mp3-duration — MP3 / JavaScript

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** mp3-duration
- **Local input API:** `mp3Duration(Buffer,callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp3-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "duration_ms": 1224
}
```

Frame duration includes MP3 padding and differs from nominal one-second source duration.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/mp3_duration/README.md)

```sh
python3 parsarium.py build mp3 javascript mp3_duration
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/id3v2-tagged-tone.mp3
```

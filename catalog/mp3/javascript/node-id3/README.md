# node-id3 — MP3 / JavaScript

- **Pinned release:** `0.2.9`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** node-id3
- **Local input API:** `read(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-id3>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/node_id3/README.md)

```sh
python3 parsarium.py build mp3 javascript node_id3
python3 parsarium.py run mp3 javascript node_id3 controls/mp3/id3v2-tagged-tone.mp3
```

# simple-id3.js — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** simple-id3.js
- **Local input API:** `new ID3(Uint8Array).asObject()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/simple-id3.js>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

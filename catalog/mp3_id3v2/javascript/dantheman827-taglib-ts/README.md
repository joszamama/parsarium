# @dantheman827/taglib-ts — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.1.5`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** tags
- **Underlying family:** TagLib TypeScript port
- **Local input API:** `readTags(Uint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@dantheman827/taglib-ts>)
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

TypeScript port of TagLib, distinct from native C++ implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

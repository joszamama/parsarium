# mp3tag.js — MP3 with ID3v2 / JavaScript

- **Pinned release:** `3.17.1`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** mp3tag.js
- **Local input API:** `new MP3Tag(Buffer).read()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp3tag.js>)
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

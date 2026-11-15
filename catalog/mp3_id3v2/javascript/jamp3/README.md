# jamp3 — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.6.1`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** jamp3
- **Local input API:** `new ID3v2().read(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/jamp3>)
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

# @shapes-org/node-id3 — MP3 with ID3v2 / JavaScript

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** tags
- **Underlying family:** node-id3
- **Local input API:** `read(Buffer)`
- **Documentation:** [API reference](<https://unpkg.com/@shapes-org/node-id3@0.2.0/dist/src/api/read.d.ts>)
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

Documented fork of node-id3, same parser lineage.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.

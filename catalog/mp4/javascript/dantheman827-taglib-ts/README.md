# @dantheman827/taglib-ts — MP4 / JavaScript

- **Pinned release:** `0.1.5`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** tags+audio_properties
- **Underlying family:** TagLib TypeScript port
- **Local input API:** `readTags(Uint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@dantheman827/taglib-ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "sampleRate": 8000,
  "channels": 1
}
```

TypeScript port of TagLib; shared design lineage, not the native C++ implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
